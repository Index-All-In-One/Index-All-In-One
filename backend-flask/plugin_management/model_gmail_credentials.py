from sqlalchemy import orm, sqlalchemy_db
from sqlalchemy import create_engine, Column, Integer, String, select
model = orm.declarative_base()

class GmailCredentials(model):
    __tablename__ = 'gmail_credentials'
    id = sqlalchemy_db.Column(sqlalchemy_db.Integer, primary_key=True)
    plugin_instance_id = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=True)
    username = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=False)
    password = sqlalchemy_db.Column(sqlalchemy_db.String(50), nullable=False)

class Credentials(model):
    __tablename__ = 'gmail_credentials'

    id = Column(Integer, primary_key=True)
    task_op = Column(String(20), nullable=False)
    plugin_instance_id = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)

    def __init__(self, task_op, plugin_instance_id, status):
        self.task_op = task_op
        self.plugin_instance_id = plugin_instance_id
        self.status = status
        
__all__ = ['model', 'GmailCredentials', 'Credentials']

