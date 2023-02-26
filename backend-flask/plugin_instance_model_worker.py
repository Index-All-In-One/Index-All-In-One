import sqlalchemy as sqlalchemy_db
from sqlalchemy.ext.declarative import declarative_base

model = sqlalchemy_db.orm.declarative_base()

class Request(model):
    __tablename__ = 'request'
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    request_op = sqlalchemy_db.Column(sqlalchemy_db.String(20), nullable=False)
    plugin_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=True)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), unique=True, nullable=True)
    update_interval = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=True)


__all__ = ['model', 'Request']
