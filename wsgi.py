#!/usr/bin/env python3
import click
from flask import Flask, redirect, render_template, request, make_response
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin
from sqlalchemy.orm import Session, scoped_session
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import fields, validators

from models import db, MyUser

import os
import shutil
import glob
import re
from typing import Union

# ===================================初始化Flask Start========================#
app: Flask = Flask(__name__)

app.config["SECRET_KEY"] = "SystemLight"
app.config["JSON_AS_ASCII"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://trial:df2wDr8jSFw6cCkL@192.168.52.181/trial"
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"

db.init_app(app)
session: Union[Session, scoped_session] = db.session

migrate = Migrate(app, db)


# ===================================初始化Flask END========================#


# ===================================数据模型 Start========================#
class UserAuth(UserMixin):

    def __init__(self, user_model: MyUser):
        self.user_model: MyUser = user_model

    def get_id(self) -> int:
        return self.user_model.id

    def verify_password(self, password: str) -> bool:
        if self.user_model.password != password:
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


class LoginForm(FlaskForm):
    phone = fields.StringField("手机号", validators=[validators.DataRequired()])
    password = fields.PasswordField("密码", validators=[validators.DataRequired()])


class ResponseResult:

    def __init__(self, code=200, msg="ok", data=None):
        self.code = code
        self.msg = msg
        self.data = data


# ===================================数据模型 End========================#


# ===================================Flask Hook========================#
@login_manager.user_loader
def load_user(userid):
    return UserAuth.get(userid)


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


# ===================================Flask Hook========================#


# ===================================普通路由========================#
@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


@app.route("/protect_route", methods=["GET"])
@login_required
def protect_route():
    return {"msg": "ok"}


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    err_msg = None

    if form.validate_on_submit():
        phone = form.phone.data
        password = form.password.data
        user = UserAuth.get_by_phone(phone)
        if user is None:
            err_msg = "用户不存在"
        else:
            if user.verify_password(password):
                login_user(user)
                return redirect(request.args.get("next") or "/")
            else:
                err_msg = "用户密码错误"

    return render_template("login.html", form=form, emsg=err_msg)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/")


# ===================================普通路由========================#


# ===================================公共函数区域========================#

# ===================================公共函数区域========================#


if __name__ == '__main__':
    app.run(host="localhost", port=6666)
