from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_op = db.Column(db.String(20), nullable=False)
    plugin_name = db.Column(db.String(120), nullable=True)
    plugin_instance_id = db.Column(db.String(50), unique=True, nullable=True)
    update_interval = db.Column(db.Integer, nullable=True)

__all__ = ['db']
