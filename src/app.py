#!/usr/bin/env python3
from flask import Flask

from mvc import use_mvc

app: Flask = Flask(__name__)
app.secret_key = "SystemLight"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
use_mvc(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def spa(path):
    """

    SPA单页应用路由

    :param path:
    :return:

    """
    return app.send_static_file("index.html")


@app.errorhandler(400)
def bad_request(e):
    """

    集中处理400错误

    :param e:
    :return:

    """
    data = getattr(e, "data", None)
    if data:
        return {"data": data, "code": e.code}
    return e


@app.cli.command("initdb")
def init_db():
    """

    注册flask命令行初始化数据库

    :return:

    """
    ...


if __name__ == '__main__':
    app.run()
