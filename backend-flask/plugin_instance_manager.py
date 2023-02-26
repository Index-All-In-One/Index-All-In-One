import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from plugin_instance_model_worker import *


def PI_db_test(session):
    # Use the session to interact with the database
    requests = session.query(Request).all()
    for row in requests:
        print(row.id, row.request_op, row.plugin_name, row.plugin_instance_id, row.update_interval)

    query = select(*[Request.id, Request.request_op, Request.plugin_name, Request.plugin_instance_id, Request.update_interval]).order_by(Request.id).limit(1)
    print(query)
    request=session.execute(query).fetchone()
    print(request)

def init_db():
    engine = create_engine('sqlite:///instance/PI.db')
    model.metadata.bind = engine
    model.metadata.create_all(engine)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

def start_plugin_instances(session):
    pass

def get_request(session):
    query = select(*[Request.id, Request.request_op, Request.plugin_name, Request.plugin_instance_id, Request.update_interval]).order_by(Request.id).limit(1)
    request=session.execute(query).fetchone()
    return request

def handle_request(session, request):
    if request is None:
        return
    if request.request_op == 'add':
        print('Add plugin instance: ', request.plugin_name, request.update_interval)
    elif request.request_op == 'del':
        print('Delete plugin instance: ', request.plugin_instance_id)
    else:
        print('Unknown request: ', request.request_op)

    session.query(Request).filter(Request.id == request.id).delete()
    session.commit()

def loop_for_request(session):
    while True:
        request = get_request(session)
        handle_request(session, request)
        time.sleep(0.5)

if __name__ == "__main__":
    session = init_db()
    start_plugin_instances(session)
    loop_for_request(session)
