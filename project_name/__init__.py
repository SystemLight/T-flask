from flask import Flask, redirect, render_template, request
from flask_login import LoginManager, login_required, logout_user, login_user, current_user, AnonymousUserMixin
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .db import db, session
from . import routes
from . import cli
from . import models
from .models.login_form import LoginForm
from .models.user_auth import UserAuth

app: Flask = Flask(__name__)
app.config.from_pyfile("config.py")

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return UserAuth.get(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    if not isinstance(current_user, AnonymousUserMixin):
        return redirect("/")

    form = LoginForm()
    err_msg = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = UserAuth.get_by_name(username)
        if user is None:
            err_msg = "用户不存在"
        else:
            if user.verify_password(password):
                login_user(user)
                return redirect(request.args.get("next") or "/")
            else:
                err_msg = "用户密码错误"
    return render_template("login.html", form=form, emsg=err_msg)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


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


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def spa_route(path: str):
    """

    定义SPA单页应用路由

    :param path:
    :return:

    """
    return app.send_static_file("index.html")


migrate = Migrate(app, db)
# admin = Admin(app, name="后台管理", template_mode="bootstrap4")
# admin.add_view(ModelView(models.person.Person, session))

cli.init_app(app)
db.init_app(app)
routes.init_app(app)
