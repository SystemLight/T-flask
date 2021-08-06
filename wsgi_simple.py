#!/usr/bin/env python3
import os
import uuid
from datetime import datetime
from typing import Union

import click
from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session, scoped_session
from werkzeug.security import safe_join

"""

简化版本的T-flask，用于开发轻量应用

"""

# region===================================初始化========================#
app: Flask = Flask(__name__)

app.config["SECRET_KEY"] = "SystemLight"
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
session: Union[Session, scoped_session] = db.session
migrate = Migrate(app, db)

STANDARD_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# endregion===================================初始化========================#


# region===================================数据模型========================#


# endregion===================================数据模型========================#


# region===================================Flask钩子========================#
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
    return render_template("home.html")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return app.send_static_file("index.html")


# endregion===================================注册路由========================#


# region===================================公共函数========================#
def now():
    return datetime.now().strftime(STANDARD_TIME_FORMAT)


def dt2str(dt: datetime):
    return dt.strftime(STANDARD_TIME_FORMAT)


def safe_strftime(dt: datetime):
    if isinstance(dt, datetime):
        return dt.strftime(STANDARD_TIME_FORMAT)
    return ""


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


def make_error(msg="error", code=400, data=None):
    return {"code": code, "msg": msg, "data": data}, code


def make_unauthorized(msg="error", code=401, data=None):
    return make_error(msg, code, data)


def make_ok(msg="ok", code=200, data=None):
    return {"code": code, "msg": msg, "data": data}, code


# endregion===================================公共函数========================#

if __name__ == '__main__':
    app.run(host="localhost", port=5555)
