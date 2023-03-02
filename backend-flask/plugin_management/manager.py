import time
import threading
import uuid
import logging
import sys
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model_standalone import *
import threading
import uuid
from plugins.entry import dispatch_plugin

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def plugin_instance_routine(session, opensearch_hostname, plugin_name, plugin_instance_id, run_id, update_interval):
    counter = 0
    while True:
        running_instance = session.query(RunningPluginInstance).filter(RunningPluginInstance.run_id == run_id).first()
        if running_instance is None:
            logging.debug("[%d] Routine: %s %s %s %d is terminated", counter, plugin_name, plugin_instance_id, run_id, update_interval)
            break
        logging.debug("[%d] Routine: %s %s %s %d is running", counter, plugin_name, plugin_instance_id, run_id, update_interval)
        dispatch_plugin("", "update", plugin_name, [opensearch_hostname, plugin_instance_id])
        counter += 1
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
    session.query(RunningPluginInstance).delete()
    session.commit()
    return DBSession

def start_plugin_instances(DBSession):
    session = DBSession()
    pass

def get_request(session):
    query = select(*[Request.id, Request.request_op, Request.plugin_name, Request.plugin_instance_id, Request.update_interval]).order_by(Request.id).limit(1)
    request=session.execute(query).fetchone()
    return request

def handle_request(DBSession, man_session, request):
    global opensearch_hostname
    if request is None:
        return
    if request.request_op == 'activate':
        logging.debug('Manager: Activate plugin instance Request: %s %s %d', request.plugin_name, request.plugin_instance_id, request.update_interval)

        run_id=str(uuid.uuid4())
        plugin_instance = man_session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == request.plugin_instance_id).first()

        if plugin_instance is not None:
            running_plugin_instance = RunningPluginInstance(plugin_instance_id=request.plugin_instance_id, run_id=run_id)
            man_session.add(running_plugin_instance)
            man_session.commit()

            routine_thread = threading.Thread(target=plugin_instance_routine, args=(DBSession(), opensearch_hostname, request.plugin_name, request.plugin_instance_id, run_id, request.update_interval))
            routine_thread.start()
            plugin_instance.active = True

    elif request.request_op == 'deactivate':
        logging.debug('Manager: Deactivate plugin instance Request: %s ', request.plugin_instance_id)

        man_session.query(RunningPluginInstance).filter(RunningPluginInstance.plugin_instance_id == request.plugin_instance_id).delete()

        plugin_instance = man_session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == request.plugin_instance_id).first()
        if plugin_instance is not None:
            plugin_instance.active = False
            man_session.query(RunningPluginInstance).filter(RunningPluginInstance.plugin_instance_id == request.plugin_instance_id).delete()

    elif request.request_op == 'change_interval':
        pass
    else:
        logging.debug('Manager: Unknown request: %s', request.request_op)

    man_session.query(Request).filter(Request.id == request.id).delete()
    man_session.commit()

def loop_for_request(DBSession):
    man_session = DBSession()
    while True:
        request = get_request(man_session)
        handle_request(DBSession, man_session, request)
        time.sleep(0.3)

if __name__ == "__main__":
    opensearch_hostname = os.environ.get('OPENSEARCH_HOSTNAME', 'localhost')
    DBSession = init_db("PI.db")
    start_plugin_instances(DBSession)
    loop_for_request(DBSession)
