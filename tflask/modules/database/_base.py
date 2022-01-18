from typing import Union

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session, scoped_session

from ...context import app

db = SQLAlchemy(app)
session: Union[Session, scoped_session] = db.session
migrate = Migrate(app, db)
