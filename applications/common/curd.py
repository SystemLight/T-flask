import datetime

from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..extensions import db, ma


class LogicalDeleteMixin:
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    delete_at = db.Column(db.DateTime, comment='删除时间')


def model_to_dicts(model: db.Model, data):
    """

    不需要建立schemas，直接使用orm的定义模型进行序列化
    基本功能，待完善

    示例::

        power_data = curd.auto_model_jsonify(model=Dept, data=dept)

    """

    def get_model():
        return model

    class AutoSchema(SQLAlchemyAutoSchema):
        class Meta(Schema):
            model = get_model()
            include_fk = True
            include_relationships = True
            load_instance = True

    return AutoSchema(many=True).dump(data)


def schema_to_dicts(schema: ma.Schema, data):
    return schema(many=True).dump(data)


def get_one_by_id(model: db.Model, iid):
    return model.query.filter_by(id=iid).first()


def delete_one_by_id(model: db.Model, iid):
    r = model.query.filter_by(id=iid).delete()
    db.session.commit()
    return r


def enable_status(model: db.Model, iid):
    role = model.query.filter_by(id=iid).update({"enable": 1})
    if role:
        db.session.commit()
        return True
    return False


def disable_status(model: db.Model, iid):
    role = model.query.filter_by(id=iid).update({"enable": 0})
    if role:
        db.session.commit()
        return True
    return False
