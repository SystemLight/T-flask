from flask import render_template
from flask_login import login_required

from ._base import bp, api, Resource


@bp.route("/hello")
@login_required
def hello():
    return {"msg": "ok"}


@bp.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@bp.route("/td", methods=["GET"])
def trial_db():
    return "ok"


@api.resource("/home")
class HomeApi(Resource):

    def get(self):
        return {"msg": "hello"}
