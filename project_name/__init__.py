import click
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .db import db, session
from . import models
from . import routes

app: Flask = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def spa(path):
    """

    SPA单页应用路由

    :param path:
    :return:

    """
    return app.send_static_file("index.html")


@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


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


migrate = Migrate(app, db)
admin = Admin(app, name="后台管理", template_mode="bootstrap4")
admin.add_view(ModelView(models.person.Person, session))
db.init_app(app)
routes.init_app(app)
