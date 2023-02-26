import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from plugin_instance_model_worker import *
import threading
import uuid
from plugins.plugin_entry import dispatch_plugin

def plugin_instance_routine(plugin_name, plugin_instance_id, run_id, update_interval):
    while True:
        running_instance = session.query(RunningPluginInstance).filter(RunningPluginInstance.run_id == run_id).first()
        if running_instance is None:
            print('Routine: ', plugin_name, plugin_instance_id, run_id, update_interval, ' is terminated')
            break
        print("Routine: ", plugin_name, plugin_instance_id, run_id, update_interval, ' is running')
        dispatch_plugin(plugin_name, [plugin_instance_id])
        time.sleep(update_interval)


def PI_db_test(session):
    # Use the session to interact with the database
    requests = session.query(Request).all()
    for row in requests:
        print(row.id, row.request_op, row.plugin_name, row.plugin_instance_id, row.update_interval)

    query = select(*[Request.id, Request.request_op, Request.plugin_name, Request.plugin_instance_id, Request.update_interval]).order_by(Request.id).limit(1)
    print(query)
    request=session.execute(query).fetchone()
    print(request)

def init_db(db_name):
    engine = create_engine(f'sqlite:///instance/{db_name}')
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
        print('Manager: Add plugin instance Request: ', request.plugin_name, request.update_interval)
        plugin_instance_id=str(uuid.uuid4())
        run_id=str(uuid.uuid4())
        # TODO: check and mod "all" table
        running_plugin_instance = RunningPluginInstance(plugin_instance_id=plugin_instance_id, run_id=run_id)
        routiine_thread = threading.Thread(target=plugin_instance_routine, args=(request.plugin_name, plugin_instance_id, run_id, request.update_interval))
        session.add(running_plugin_instance)
        session.commit()
        routiine_thread.start()
    elif request.request_op == 'del':
        print('Manager: Delete plugin instance Request: ', request.plugin_instance_id)
        #TODO: delete from "all" table
        session.query(RunningPluginInstance).filter(RunningPluginInstance.plugin_instance_id == request.plugin_instance_id).delete()
    else:
        print('Unknown request: ', request.request_op)

    session.query(Request).filter(Request.id == request.id).delete()
    session.commit()

def loop_for_request(session):
    while True:
        request = get_request(session)
        handle_request(session, request)
        time.sleep(0.3)

if __name__ == "__main__":
    session = init_db("PI.db")
    start_plugin_instances(session)
    loop_for_request(session)
