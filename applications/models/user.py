from ..extensions import db
from ._utils import get_auto_schema


class UserModel(db.Model):
    __tablename__ = 't_user'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), default='')
    age = db.Column(db.Integer, default=0)


UserSchema = get_auto_schema(UserModel)
