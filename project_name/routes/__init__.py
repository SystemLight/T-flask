from ._base import bp
from . import home


def init_app(app):
    app.register_blueprint(bp)
