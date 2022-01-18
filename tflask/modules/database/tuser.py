from ._base import db


class TUser(db.Model):
    __tablename__ = 't_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    create_at = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
