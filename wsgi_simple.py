#!/usr/bin/env python3
import os
import shutil
from datetime import datetime
from typing import Union

import click
from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session, scoped_session

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

    def __init__(self, _on_finished=None):
        self.total_chunks = None
        self.offset = None

        self.chunk_block = None
        self.chunk_id = None

        self.file_id = None
        self.file_name = None
        self.file_size = None

        self._on_finished = _on_finished

        self.url_prefix = "/static/"

    @staticmethod
    def from_flask_request(_on_finished=None):
        options = ChunkOptions(_on_finished)

        options.total_chunks = int(request.form["totalChunks"])  # 总计块数量
        options.offset = int(request.form["offset"])  # 文件偏移位置

        options.chunk_block = request.files["chunkBlock"]  # 当前块内容
        options.chunk_id = int(request.form["chunkID"])  # 当前块编号

        options.file_id = request.form["fileID"]  # 块存储唯一ID
        options.file_name = request.form["fileName"]  # 文件原始名称
        options.file_size = int(request.form["fileSize"])  # 文件原始总大小

        return options

    def is_end_block(self):
        """

        判定当前块是否为最终块

        :return:

        """
        return self.chunk_id + 1 == self.total_chunks

    def render_url(self):
        return f"{self.url_prefix}{self.file_name}"

    def on_process(self, result, save_path):
        """

        进程块保存完毕时回调处理

        :param save_path:
        :param result:
        :return:

        """
        pass

    def on_finished(self, result, save_path):
        """

        最终块保存完毕时回调处理

        :param save_path:
        :param result:
        :return:

        """
        if callable(self._on_finished):
            self._on_finished(self, result, save_path)


class SliceSaveFile:

    def __init__(self, options: ChunkOptions):
        self.options = options
        self.save_path = f"static/{options.file_name}"

    def is_exists(self):
        if os.path.exists(self.save_path) and self.options.chunk_id == 0:
            return True
        return False

    def save(self):
        if self.is_exists():
            raise ExistsError("文件已经存在")
        with open(self.save_path, "ab") as f:
            f.seek(self.options.offset)
            f.write(self.options.chunk_block.stream.read())

        result = {
            "name": self.options.file_name,
            "url": self.options.render_url(),
            "uid": self.options.file_id,
            "status": "success"
        }

        if self.options.is_end_block():
            if os.path.getsize(self.save_path) != self.options.file_size:
                raise UploadError("上传失败")
            self.options.on_finished(result, self.save_path)
        else:
            self.options.on_process(result, self.save_path)

        return result


def make_error(msg="error", code=400, data=None):
    return {"code": code, "msg": msg, "data": data}, code


def make_unauthorized(msg="error", code=401, data=None):
    return make_error(msg, code, data)


def make_ok(msg="ok", code=200, data=None):
    return {"code": code, "msg": msg, "data": data}, code


# endregion===================================公共函数========================#

if __name__ == '__main__':
    app.run(host="localhost", port=5555)
