from flask import Blueprint, render_template

hello_views = Blueprint("hello", __name__)


@hello_views.route("/hello")
def hello():
    return render_template("hello.html", name="Hello")
