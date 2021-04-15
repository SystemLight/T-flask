import click
from flask import Flask
from flask_migrate import Migrate

from .db import db
from . import models
from . import routes

app: Flask = Flask(__name__)
migrate = Migrate()


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

    init the app database.

    """
    if drop:
        click.confirm("This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo("Drop tables.")
    db.create_all()
    click.echo("Initialized database.")


app.config["SECRET_KEY"] = "SystemLight"
app.config["JSON_AS_ASCII"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)
routes.init_app(app)
