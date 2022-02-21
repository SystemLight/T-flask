from flask import Flask

from .init_dotenv import init_dotenv
from .init_error_views import init_error_views
from .init_migrate import init_migrate
from .init_scripts import init_scripts
from .init_sqlalchemy import init_databases, db, ma


def init_plugs(app: Flask) -> None:
    init_dotenv()
    init_databases(app)
    init_migrate(app, db)
    init_scripts(app, db)
    init_error_views(app)
