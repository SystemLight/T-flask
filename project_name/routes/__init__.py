from flask import Flask

from ._base import bp
from . import home


def init_app(app: Flask):
    app.register_blueprint(bp)
