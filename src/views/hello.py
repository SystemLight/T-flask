from flask import Blueprint

hello_blueprint = Blueprint("hello", __name__)


@hello_blueprint.route("/say_hello")
def say_hello():
    return "hello"
