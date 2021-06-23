from flask_login import UserMixin

from .person import Person
from ..db import session


class UserAuth(UserMixin):

    def __init__(self, user_model):
        self.user_model: Person = user_model

    def get_id(self):
        return self.user_model.id

    def verify_password(self, password):
        if self.user_model.name != password:
            return False
        return True

    @staticmethod
    def get(user_id):
        model = session.get(Person, user_id)
        if model:
            return UserAuth(model)
        return None

    @staticmethod
    def get_by_name(user_name):
        model = session.query(Person).filter(Person.name == user_name).first()
        if model:
            return UserAuth(model)
        return None
