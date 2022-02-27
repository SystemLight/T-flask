from .db import init_db


def init_scripts(app):
    init_db(app)
