import sqlalchemy as sqlalchemy_db
from sqlalchemy.ext.declarative import declarative_base

model = sqlalchemy_db.orm.declarative_base()

class Request(model):
    __tablename__ = 'request'
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    request_op = sqlalchemy_db.Column(sqlalchemy_db.String(20), nullable=False)
    plugin_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=True)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=True)
    update_interval = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=True)

class RunningPluginInstance(model):
    __tablename__ = 'running_plugin_instance'
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=True)
    run_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), unique=True, nullable=True)

class PluginInstance(model):
    __tablename__ = 'plugin_instance'
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    plugin_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=False)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), unique=True, nullable=False)
    source_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=False)
    update_interval = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=False)
    enabled = sqlalchemy_db.Column(sqlalchemy_db.Boolean, nullable=False, default=True)
    active = sqlalchemy_db.Column(sqlalchemy_db.Boolean, nullable=False, default=False)

__all__ = ['model', 'Request', 'RunningPluginInstance', 'PluginInstance']
