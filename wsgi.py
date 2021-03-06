#!/usr/bin/env python3
import os
import re
import glob
import shutil
import uuid
from datetime import datetime
from typing import Union

import click
import requests
from flask import Flask, redirect, render_template, request, session as f_session
from flask_login import LoginManager, login_required, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import safe_join
from itsdangerous import TimedJSONWebSignatureSerializer, BadData
from sqlalchemy import func, text
from sqlalchemy.orm import Session, scoped_session
from marshmallow import Schema, fields as m_fields

# region===================================初始化========================#
app: Flask = Flask(__name__)

app.config["SECRET_KEY"] = "SystemLight"
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://trial:df2wDr8jSFw6cCkL@192.168.52.181/trial"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)
session: Union[Session, scoped_session] = db.session
migrate = Migrate(app, db)
jwt_ser = TimedJSONWebSignatureSerializer(secret_key=app.config["SECRET_KEY"], expires_in=2592000)


# endregion===================================初始化========================#


# region===================================数据模型========================#
class MyUser(db.Model):
    __tablename__ = 'my_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    create_at = db.Column(db.DateTime)
    priority = db.Column(db.Integer)


class UserAuth(UserMixin):

    def __init__(self, model: MyUser):
        self.model: MyUser = model

    def get_id(self) -> int:
        return self.model.id

    def verify_password(self, password: str) -> bool:
        if self.model.password != password:
            return False
        return True

    @staticmethod
    def get(user_id: int):
        model = session.get(MyUser, user_id)
        if model:
            return UserAuth(model)
        return None

    @staticmethod
    def get_by_phone(phone: str):
        model = session.query(MyUser).filter(MyUser.phone == phone).first()
        if model:
            return UserAuth(model)
        return None


# endregion===================================数据模型========================#


# region===================================Flask钩子========================#
@login_manager.request_loader
def request_loader(req):
    token = req.headers.get("Authorization", None)
    if token and token.startswith("Bearer "):
        token = token[7:len(token)]
        try:
            token = jwt_ser.loads(token)
            return UserAuth.get(token["user_id"])
        except BadData:
            ...
    return None


@login_manager.unauthorized_handler
def unauthorized_handler():
    return make_unauthorized("权限校验失败")


@app.cli.command("initdb")
@click.option("--drop", is_flag=True, help="Create after drop.")
def init_db(drop):
    """

    init the app database.

    """
    if drop:
        click.confirm("This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo("Drop tables.")
    db.create_all()
    click.echo("Initialized database.")


# endregion===================================Flask Hook========================#


# region===================================注册路由========================#
@app.route("/", methods=["GET"])
def index():
    """

    主页

    :return:

    """
    return app.send_static_file("index.html")


@app.route("/api/user/<uid>", methods=["GET"])
def get_user(uid):
    """

    [api]-获取指定用户信息

    :param uid:
    :return:

    """
    return {}


@app.route("/api/user/<uid>", methods=["POST"])
def set_user(uid):
    """

    [api]-修改指定用户信息

    :param uid:
    :return:

    """
    return {}


@app.route("/api/upload_demo", methods=["POST"])
def upload_demo():
    """

    [api]-分片文件上传，注意Flask开发服务器如果上传请求次数过多会超时，导致上传失败

    :return:

    """
    try:
        file = SliceSaveFile("./static/files", "/static/files/", ChunkOptions.from_flask_request())
        result = file.save()
    except Exception as e:
        return make_error(str(e))
    return make_ok(data=result)


@app.route("/api/oauth/captcha", methods=["POST"])
def send_sms():
    """

    [api]-发送短信

    :return:

    """
    phone = request.form["phone"]
    return make_ok()


@app.route("/api/login", methods=["POST"])
def login():
    """

    [api]-用户登录

    :return:

    """
    phone = request.form["phone"]
    code = request.form["code"]

    user_auth = UserAuth.get_by_phone(phone)
    if user_auth:
        user = user_auth.model
    else:
        try:
            user = MyUser(name=phone, phone=phone, password=code)
            session.add(user)
        except Exception as e:
            session.rollback()
            return make_error(str(e))
        else:
            session.commit()

    return make_ok(data={"token": jwt_ser.dumps({"user_id": user.id}).decode()})


@app.route("/api/register", methods=["POST"])
def register():
    """

    [api]-用户注册

    :return:
    """


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    """

    [api]-用户退出登录

    :return:

    """
    return make_ok()


# endregion===================================注册路由========================#


# region===================================公共函数========================#
STANDARD_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def now():
    return datetime.now().strftime(STANDARD_TIME_FORMAT)


def dt2str(dt: datetime):
    return dt.strftime(STANDARD_TIME_FORMAT)


def safe_strftime(dt: datetime):
    if isinstance(dt, datetime):
        return dt.strftime(STANDARD_TIME_FORMAT)
    return ""


def make_error(msg="error", code=400, data=None):
    return {"code": code, "msg": msg, "data": data}, code


def make_unauthorized(msg="error", code=401, data=None):
    return make_error(msg, code, data)


def make_ok(msg="ok", code=200, data=None):
    return {"code": code, "msg": msg, "data": data}, code


class ExistsError(Exception):
    ...


class UploadError(Exception):
    ...


class ChunkOptions:

    def __init__(self):
        self.total_chunks = None
        self.offset = None

        self.chunk_block = None
        self.chunk_id = None

        self.file_id = None
        self.file_name = None
        self.file_size = None

    def is_end_block(self):
        return self.chunk_id + 1 == self.total_chunks

    @staticmethod
    def from_flask_request():
        options = ChunkOptions()

        options.total_chunks = int(request.form["totalChunks"])  # 总计块数量
        options.offset = int(request.form["offset"])

        options.chunk_block = request.files["chunkBlock"]
        options.chunk_id = int(request.form["chunkID"])  # 当前块编号

        options.file_id = request.form["fileID"]
        options.file_name = request.form["fileName"]
        options.file_size = int(request.form["fileSize"])

        return options


class SliceSaveFile:

    def __init__(self, save_folder: str, url_prefix: str, options: ChunkOptions):
        self.options = options

        self.file_name, self.file_ext = os.path.splitext(options.file_name)
        self.save_file_name = f"{options.file_id}{self.file_ext}"
        self.save_path = safe_join(save_folder, self.save_file_name)
        self.url_path = f"{url_prefix}{self.save_file_name}"

    def save(self):
        if self.is_exists():
            raise ExistsError("文件已经存在")

        with open(self.save_path, "ab") as f:
            f.seek(self.options.offset)
            f.write(self.options.chunk_block.stream.read())

        if self.options.is_end_block():
            if os.path.getsize(self.save_path) != self.options.file_size:
                raise UploadError("上传失败")

        return {
            "name": self.file_name,
            "url": self.url_path,
            "uid": str(uuid.uuid1()),
            "status": "success"
        }

    def is_exists(self):
        if os.path.exists(self.save_path) and self.options.chunk_id == 0:
            return True
        return False


# endregion===================================公共函数========================#

if __name__ == '__main__':
    app.run(host="localhost", port=5555)
