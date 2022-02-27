from flask import Flask

from .init_dotenv import init_dotenv
from .init_model import init_model, db, ma
from .init_error_views import init_error_views
from .flask_sse import init_sse, sse
from .flask_background import Task


def init_plugs(app: Flask) -> None:
    init_dotenv()
    init_model(app)
    init_error_views(app)
    init_sse(app)
