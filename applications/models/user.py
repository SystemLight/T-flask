from ..extensions import db


class TUserModel(db.Model):
    __tablename__ = 'tuser'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), default='')
    age = db.Column(db.Integer, default=0)
