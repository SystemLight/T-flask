from flask import Flask

from .init_dotenv import init_dotenv
from .init_error_views import init_error_views
from .init_scripts import init_scripts
from .init_model import init_model, db, ma


def init_plugs(app: Flask) -> None:
    init_dotenv()
    init_model(app)
    init_scripts(app, db)
    init_error_views(app)
