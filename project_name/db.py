from sqlalchemy.orm import Session, scoped_session
from flask_sqlalchemy import SQLAlchemy

from typing import Union

db = SQLAlchemy()
session: Union[Session, scoped_session] = db.session
