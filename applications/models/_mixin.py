import datetime

from ..extensions import db


class LogicalDeleteMixin:
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='修改时间')
    delete_at = db.Column(db.DateTime, comment='删除时间')
