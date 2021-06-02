from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .db import db, session
from . import models
from . import routes
from . import cli
from . import interceptor

app: Flask = Flask(__name__)
app.config.from_pyfile("config.py")

migrate = Migrate(app, db)
admin = Admin(app, name="后台管理", template_mode="bootstrap4")
admin.add_view(ModelView(models.person.Person, session))

interceptor.init_app(app)
cli.init_app(app)
db.init_app(app)
routes.init_app(app)
