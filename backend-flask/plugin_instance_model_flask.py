from flask_sqlalchemy import SQLAlchemy

sqlalchemy_db = SQLAlchemy()
model = sqlalchemy_db.Model

class Request(model):
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    request_op = sqlalchemy_db.Column(sqlalchemy_db.String(20), nullable=False)
    plugin_name = sqlalchemy_db.Column(sqlalchemy_db.String(120), nullable=True)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=True)
    update_interval = sqlalchemy_db.Column(sqlalchemy_db.Integer, nullable=True)

__all__ = ['sqlalchemy_db', 'Request']
