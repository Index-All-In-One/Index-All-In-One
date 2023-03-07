import time
import threading
import uuid
import logging
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model_standalone import *
from plugins.entry_plugin import dispatch_plugin
from plugins.status_code import PluginReturnStatus
from opensearch.conn import check_index_exist

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def plugin_instance_routine(session, opensearch_hostname, plugin_name, plugin_instance_id, run_id, update_interval):
    counter = 0
    while True:
        running_instance = session.query(RunningPluginInstance).filter(RunningPluginInstance.run_id == run_id).first()
        if running_instance is None:
            PI_instance = session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
            if PI_instance is None:
                #TODO: send delete request to opensearch
                logging.debug("[%d] Routine: %s %s %s %d sent delete all docs request", counter, plugin_name, plugin_instance_id, run_id, update_interval)
                pass
            logging.debug("[%d] Routine: %s %s %s %d is terminated", counter, plugin_name, plugin_instance_id, run_id, update_interval)
            break

        #TODO return status code for plugin update failure
        try:
            status = dispatch_plugin("update", plugin_name, [plugin_instance_id, opensearch_hostname, ])
        except Exception as e:
            logging.error(e)
            status = PluginReturnStatus.EXCEPTION

        if status == PluginReturnStatus.SUCCESS:
            logging.debug("[%d] Routine: %s %s %s %d run update successfully", counter, plugin_name, plugin_instance_id, run_id, update_interval)
        else:
            # TODO: handle plugin update failure
            logging.error("[%d] Routine: %s %s %s %d run update failed! Status: %s", counter, plugin_name, plugin_instance_id, run_id, update_interval, status.name)
            if status == PluginReturnStatus.EXCEPTION:
                # TODO: leave message in database
                all_running_instance = session.query(RunningPluginInstance).filter(RunningPluginInstance.plugin_instance_id == plugin_instance_id)
                PI_instance = session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
                if all_running_instance is not None and PI_instance is not None:
                    PI_instance.active = False
                    session.commit()
                break
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

def start_plugin_instances(DBSession, sleep_interval):
    global opensearch_hostname
    while(not check_index_exist(opensearch_hostname)):
        logging.debug('Manager: Waiting for opensearch to start')
        time.sleep(sleep_interval)

    session = DBSession()
    enabled_plugin_instances = session.query(PluginInstance).filter(PluginInstance.enabled == True).all()
    for plugin_instance in enabled_plugin_instances:
        logging.debug('Manager: Starting plugin instance: %s %s %d', plugin_instance.plugin_name, plugin_instance.plugin_instance_id, plugin_instance.update_interval)

        run_id=str(uuid.uuid4())
        running_plugin_instance = RunningPluginInstance(plugin_instance_id=plugin_instance.plugin_instance_id, run_id=run_id)
        session.add(running_plugin_instance)
        plugin_instance.active = True
        session.commit()

        routine_thread = threading.Thread(target=plugin_instance_routine, args=(DBSession(), opensearch_hostname, plugin_instance.plugin_name, plugin_instance.plugin_instance_id, run_id, plugin_instance.update_interval))
        routine_thread.start()
    logging.debug('Manager: All plugin instances are started')

def get_request(session):
    query = select(*[Request.id, Request.request_op, Request.plugin_name, Request.plugin_instance_id, Request.update_interval]).order_by(Request.id).limit(1)
    request=session.execute(query).fetchone()
    return request

def handle_request(DBSession, man_session, request):
    global opensearch_hostname
    if request is None:
        return
    if request.request_op == 'activate':
        logging.debug('Manager: Activating plugin instance Request: %s %s %d', request.plugin_name, request.plugin_instance_id, request.update_interval)

        plugin_instance = man_session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == request.plugin_instance_id).first()

        if plugin_instance is not None:
            run_id=str(uuid.uuid4())
            running_plugin_instance = RunningPluginInstance(plugin_instance_id=request.plugin_instance_id, run_id=run_id)
            man_session.add(running_plugin_instance)
            plugin_instance.active = True
            man_session.commit()

            routine_thread = threading.Thread(target=plugin_instance_routine, args=(DBSession(), opensearch_hostname, request.plugin_name, request.plugin_instance_id, run_id, request.update_interval))
            routine_thread.start()

    elif request.request_op == 'deactivate':
        logging.debug('Manager: Deactivating plugin instance Request: %s ', request.plugin_instance_id)

        man_session.query(RunningPluginInstance).filter(RunningPluginInstance.plugin_instance_id == request.plugin_instance_id).delete()

        plugin_instance = man_session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == request.plugin_instance_id).first()
        if plugin_instance is not None:
            plugin_instance.active = False

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
    sleep_interval = 5
    if len(sys.argv) > 1:
        sleep_interval = int(sys.argv[1])
    start_plugin_instances(DBSession, sleep_interval)
    loop_for_request(DBSession)
