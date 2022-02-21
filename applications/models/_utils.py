from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..extensions import db


def get_auto_schema(model: db.Model):
    def get_model():
        return model

    class AutoSchema(SQLAlchemyAutoSchema):
        class Meta(Schema):
            model = get_model()
            include_fk = True
            include_relationships = True
            load_instance = True

    return AutoSchema
