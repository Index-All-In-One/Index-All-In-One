from flask_sqlalchemy import SQLAlchemy

sqlalchemy_db = SQLAlchemy()
model = sqlalchemy_db.Model

class Request(model):
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    request_op = sqlalchemy_db.Column(sqlalchemy_db.String(20), nullable=False)
    plugin_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=True)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=True)
    update_interval = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=True)

class PluginInstance(model):
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    plugin_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=False)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), unique=True, nullable=False)
    source_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=False)
    update_interval = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=False)
    enabled = sqlalchemy_db.Column(sqlalchemy_db.Boolean, nullable=False, default=True)
    active = sqlalchemy_db.Column(sqlalchemy_db.Boolean, nullable=False, default=False)

__all__ = ['sqlalchemy_db', 'Request', 'PluginInstance']
