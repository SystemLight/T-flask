from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MyUser(db.Model):
    __tablename__ = 'my_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(50))
    create_at = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
