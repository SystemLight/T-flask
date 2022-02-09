import datetime

from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..extensions import db, ma


class LogicalDeleteMixin:
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    delete_at = db.Column(db.DateTime, comment='删除时间')


def model_to_dicts(model: db.Model, data, many=False):
    def get_model():
        return model

    class AutoSchema(SQLAlchemyAutoSchema):
        class Meta(Schema):
            model = get_model()
            include_fk = True
            include_relationships = True
            load_instance = True

    return AutoSchema(many=many).dump(data)


def schema_to_dicts(schema: ma.Schema, data, many=False):
    return schema(many=many).dump(data)
