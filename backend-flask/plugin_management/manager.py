import time
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from model_standalone import *
import threading
import uuid
from plugins.plugin_entry import dispatch_plugin

def plugin_instance_routine(session, plugin_name, plugin_instance_id, run_id, update_interval):
    while True:
        running_instance = session.query(RunningPluginInstance).filter(RunningPluginInstance.run_id == run_id).first()
        if running_instance is None:
            print('Routine: ', plugin_name, plugin_instance_id, run_id, update_interval, ' is terminated')
            break
        print("Routine: ", plugin_name, plugin_instance_id, run_id, update_interval, ' is running')
        dispatch_plugin("", "update", plugin_name, [plugin_instance_id])
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
    if request is None:
        return
    if request.request_op == 'activate':
        print('Manager: Activate plugin instance Request: ', request.plugin_name, request.plugin_instance_id, request.update_interval)
        run_id=str(uuid.uuid4())
        # TODO: check and mod "all" table
        plugin_instance = man_session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == request.plugin_instance_id).first()
        print(plugin_instance.plugin_name, plugin_instance.plugin_instance_id, plugin_instance.source_name, plugin_instance.update_interval, plugin_instance.enabled, plugin_instance.active)
        if plugin_instance is not None:
            running_plugin_instance = RunningPluginInstance(plugin_instance_id=request.plugin_instance_id, run_id=run_id)
            routine_thread = threading.Thread(target=plugin_instance_routine, args=(DBSession() ,request.plugin_name, request.plugin_instance_id, run_id, request.update_interval))
            man_session.add(running_plugin_instance)
            man_session.commit()
            routine_thread.start()
            plugin_instance.active = True

    elif request.request_op == 'deactivate':
        print('Manager: Delete plugin instance Request: ', request.plugin_instance_id)
        #TODO: delete from "all" table
        man_session.query(RunningPluginInstance).filter(RunningPluginInstance.plugin_instance_id == request.plugin_instance_id).delete()
    elif request.request_op == 'change_interval':
        pass
    else:
        print('Unknown request: ', request.request_op)

    man_session.query(Request).filter(Request.id == request.id).delete()
    man_session.commit()

def loop_for_request(DBSession):
    man_session = DBSession()
    while True:
        request = get_request(man_session)
        handle_request(DBSession, man_session, request)
        time.sleep(0.3)

if __name__ == "__main__":
    DBSession = init_db("PI.db")
    start_plugin_instances(DBSession)
    loop_for_request(DBSession)
