from sqlalchemy import create_engine, Column, Integer, String, select, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = orm.declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_op = Column(String(20), nullable=False)
    plugin_instance_id = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)

    def __init__(self, task_op, plugin_instance_id, status):
        self.task_op = task_op
        self.plugin_instance_id = plugin_instance_id
        self.status = status

class TaskDb:
    def __init__(self, db_name):
        engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def add_task(self, task_args):
        (task_op, plugin_instance_id) = task_args
        task = Task(task_op=task_op, plugin_instance_id=plugin_instance_id, status='queued')
        self.session.add(task)
        self.session.commit()

    def get_next_task(self):
        query = select(*[Task.id, Task.task_op, Task.plugin_instance_id]).where(Task.status == 'queued').order_by(Task.id).limit(1)
        result = self.session.execute(query).fetchone()

        if result:
            plugin_instance_id, task_op, task_args = result
            task = self.session.get(Task, plugin_instance_id)
            # task = self.session.query(Task).get(plugin_instance_id)
            task.status = 'in_progress'
            self.session.commit()
            return (task_op, task_args)
        else:
            return None

    def mark_task_complete(self, task_args):
        (task_op, plugin_instance_id) = task_args
        task = self.session.query(Task).filter_by(task_op=task_op, plugin_instance_id=plugin_instance_id).first()
        if task:
            task.status = 'complete'
            self.session.commit()

    def __del__(self):
        self.session.close()


def task_db_test():
    db = TaskDb("task_queue_test.db")
    assert db.get_next_task() == None
    db.add_task(("update", "task1"))
    assert db.get_next_task() == ("update", "task1")
    db.add_task(("update", "task2"))
    assert db.get_next_task() == ("update", "task2")
    assert db.get_next_task() == None
    db.mark_task_complete(("update", "task1"))


if __name__ == "__main__":
    task_db_test()
