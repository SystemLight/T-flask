#!/usr/bin/env python3
from flask import Flask
import click

from mvc import use_mvc
from mvc.modules import db

app: Flask = Flask(__name__)
app.secret_key = "SystemLight"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
use_mvc(app, need_migrate=False)


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
@click.option("--drop", is_flag=True, help="Create after drop.")
def init_db(drop):
    """

    注册flask命令行初始化数据库

    :return:

    """
    if drop:
        click.confirm("This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo("Drop tables.")
    db.create_all()
    click.echo("Initialized database.")


if __name__ == '__main__':
    app.run()
