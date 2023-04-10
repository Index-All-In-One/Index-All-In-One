from flask import Flask, jsonify, request, abort
import uuid
import logging
import json
import threading
import os
import sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model_flask import *
from plugins.entry_plugin import dispatch_plugin, get_allowed_plugin_display_list, get_allowed_plugin_list
from plugins.status_code import PluginReturnStatus
from opensearch.conn import OpenSearch_Conn
from utils_flask import *


opensearch_hostname = os.environ.get('OPENSEARCH_HOSTNAME', 'localhost')
opensearch_conn = OpenSearch_Conn()
opensearch_conn.connect(host=opensearch_hostname)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', 'PI.db')
sqlalchemy_db.init_app(app)
with app.app_context():
    sqlalchemy_db.create_all()

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
    return 'Welcome!'

@app.route('/test')
def test():
    data = {
        'name': 'John Doe',
        'email': 'johndoe@example.com',
        'phone': '123-456-7890'
    }
    return jsonify(data)

# Custom middleware function to add CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    return response

@app.route('/search_count', methods=['POST'])
def search_count():
    count = get_search_count(opensearch_conn, request)
    return jsonify({'count': count})

@app.route('/search', methods=['POST'])
def search():
    docs = extract_docs_from_response(get_search_results(opensearch_conn, request, include_fields=['doc_name', 'doc_type', 'link', 'plugin_instance_id', 'created_date', 'modified_date', 'summary', 'file_size']))

    search_results = []
    for doc in docs:
        plugin_instance = sqlalchemy_db.session.query(PluginInstance.source_name).filter_by(plugin_instance_id=doc['plugin_instance_id']).first()
        if plugin_instance is not None:
            source_name = plugin_instance.source_name
            search_results.append(
                {
                    "doc_name": doc['doc_name'],
                    "doc_type": doc['doc_type'],
                    "link": doc['link'],
                    "source": source_name,
                    "created_date": doc['created_date'],
                    "modified_date": doc['modified_date'],
                    "summary": doc['summary'],
                    "file_size": doc['file_size']
                })

    return jsonify(search_results)

@app.route('/add_PI', methods=['POST'])
def add_plugin_instance():
    json_data = json.loads(request.data)

    plugin_name = json_data.get('plugin_name', None)
    source_name = json_data.get('source_name', None)
    interval = json_data.get('interval', None)
    plugin_init_info = json_data.get('plugin_init_info', None)
    plugin_instance_id = json_data.get('id', None)

    if plugin_name is None:
        return abort(400, 'Missing key: plugin_name')
    if source_name is None:
        return abort(400, 'Missing key: source_name')
    if interval is None:
        return abort(400, 'Missing key: interval')
    if plugin_init_info is None:
        return abort(400, 'Missing key: plugin_init_info')

    if plugin_name not in get_allowed_plugin_list():
        return abort(400, 'Plugin not allowed!')

    if plugin_instance_id is not None:
        plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
        if plugin_instance is not None:
            return abort(400, 'Plugin instance id already exists!')
    else:
        plugin_instance_id=str(uuid.uuid4())

    new_plugin_instance = PluginInstance(plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, source_name=source_name, update_interval=interval, enabled=True, active=False, plugin_init_info=json.dumps(plugin_init_info))
    sqlalchemy_db.session.add(new_plugin_instance)

    # TODO: add log support inside plugin init

    try:
        status = dispatch_plugin("init", plugin_name, [plugin_instance_id, plugin_init_info])
    except Exception as e:
        app.logger.error(e)
        status = PluginReturnStatus.EXCEPTION

    if status == PluginReturnStatus.SUCCESS:
        sqlalchemy_db.session.commit()
        new_request = Request(request_op="activate", plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, update_interval=interval)
        sqlalchemy_db.session.add(new_request)
        sqlalchemy_db.session.commit()

        app.logger.debug("Plugin instance init Success! : %s, %s, %s", plugin_name, plugin_instance_id, str(plugin_init_info))
        return 'Add plugin instance successfully!'
    else:
        # TODO: handle plugin init failure
        app.logger.error("Plugin instance init failed! Status: %d : %s, %s, %s", status.name, plugin_name, plugin_instance_id, str(plugin_init_info))
        abort(400, 'Plugin instance init function failed!')


@app.route('/mod_PI', methods=['POST'])
def mod_plugin_instance():
    json_data = json.loads(request.data)

    source_name = json_data.get('source_name', None)
    interval = json_data.get('interval', None)
    plugin_init_info = json_data.get('plugin_init_info', None)
    plugin_instance_id = json_data.get('id', None)

    if source_name is None:
        return abort(400, 'Missing key: source_name')
    if interval is None:
        return abort(400, 'Missing key: interval')
    if plugin_init_info is None:
        return abort(400, 'Missing key: plugin_init_info')
    if plugin_instance_id is None:
        return abort(400, 'Missing key: plugin_instance_id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is None:
        return abort(400, "Plugin instance id does not exist!")

    plugin_instance.source_name = source_name
    interval_changed = (plugin_instance.update_interval != interval)
    plugin_instance.update_interval = interval
    plugin_init_info_str=json.dumps(plugin_init_info)
    info_changed = (plugin_instance.plugin_init_info != plugin_init_info_str)
    plugin_instance.plugin_init_info = plugin_init_info_str

    # TODO: add log support inside plugin init

    try:
        status = dispatch_plugin("init", plugin_instance.plugin_name, [plugin_instance_id, plugin_init_info])
    except Exception as e:
        app.logger.error(e)
        status = PluginReturnStatus.EXCEPTION

    if status == PluginReturnStatus.SUCCESS:
        sqlalchemy_db.session.commit()
        if plugin_instance.active and (interval_changed or info_changed):
            # if plugin_init_info changed, use change_interval to restart
            new_request = Request(request_op="change_interval", plugin_name=plugin_instance.plugin_name, plugin_instance_id=plugin_instance_id, update_interval=interval)
            sqlalchemy_db.session.add(new_request)
        sqlalchemy_db.session.commit()

        app.logger.debug("Plugin instance init Success! : %s, %s, %s", plugin_instance.plugin_name, plugin_instance_id, str(plugin_init_info))
        return 'Mod plugin instance successfully!'
    else:
        # TODO: handle plugin init failure, show error msg

        app.logger.error("Plugin instance init failed! Status: %d : %s, %s, %s", status.name, plugin_instance.plugin_name, plugin_instance_id, str(plugin_init_info))
        abort (400, 'Plugin instance init function failed!')
        # no db commit here



@app.route('/del_PI', methods=['POST'])
def delete_plugin_instance():
    plugin_instance_id = request.form.get('id')

    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is None:
        return 'No such plugin instance!'

    plugin_name = plugin_instance.plugin_name
    enabled = plugin_instance.enabled
    active = plugin_instance.active
    sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).delete()

    new_request = Request(request_op="deactivate", plugin_instance_id=plugin_instance_id)
    sqlalchemy_db.session.add(new_request)
    sqlalchemy_db.session.commit()

    #TODO return status code for plugin del failure
    try:
        status = dispatch_plugin("del", plugin_name, [plugin_instance_id])
    except Exception as e:
        app.logger.error(e)
        status = PluginReturnStatus.EXCEPTION

    delete_task = lambda: (
        app.logger.debug("plugin_instance_id %s delete_doc: %s", plugin_instance_id, opensearch_conn.delete_doc(plugin_instance_id=plugin_instance_id))
    )
    threading.Timer(interval = 12, function = delete_task).start()

    if status == PluginReturnStatus.SUCCESS:
        app.logger.debug("Plugin instance del Success! : %s, %s", plugin_name, plugin_instance_id)
        return 'Delete plugin instance successfully!'
    else:
        # TODO: handle plugin del failure
        app.logger.error("Plugin instance del failed! Status: %s : %s, %s", status.name, plugin_name, plugin_instance_id)
        return 'Plugin instance del function failed!'


@app.route('/enable_PI', methods=['POST'])
def enable_plugin_instance():
    plugin_instance_id = request.form.get('id')
    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is not None:
        plugin_instance.enabled = True

        new_request = Request(request_op="activate", plugin_name=plugin_instance.plugin_name, plugin_instance_id=plugin_instance_id, update_interval=plugin_instance.update_interval)
        sqlalchemy_db.session.add(new_request)
        sqlalchemy_db.session.commit()

        app.logger.debug("Plugin instance enabled: %s", plugin_instance_id)

    else:
        return 'No such plugin instance!'

    return 'Enable plugin instance successfully!'

@app.route('/disable_PI', methods=['POST'])
def disable_plugin_instance():
    plugin_instance_id = request.form.get('id')
    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is not None:
        plugin_instance.enabled = False

        new_request = Request(request_op="deactivate", plugin_name=plugin_instance.plugin_name, plugin_instance_id=plugin_instance_id, update_interval=plugin_instance.update_interval)
        sqlalchemy_db.session.add(new_request)
        sqlalchemy_db.session.commit()

        app.logger.debug("Plugin instance disabled: %s", plugin_instance_id)

    else:
        return 'No such plugin instance!'

    return 'Disable plugin instance successfully!'

@app.route('/list_accounts', methods=['GET'])
def list_accounts():
    all_PIs=sqlalchemy_db.session.query(PluginInstance).all()
    all_accounts = []
    for plugin_instance in all_PIs:
        all_accounts.append(
            {
                "plugin_name": plugin_instance.plugin_name,
                "source_name": plugin_instance.source_name,
                "update_interval": plugin_instance.update_interval,
                "enabled": plugin_instance.enabled,
                "active": plugin_instance.active,
                "id": plugin_instance.plugin_instance_id,
            })
    return jsonify(all_accounts)

@app.route('/plugin_list', methods=['GET'])
def get_plugin_list():
    return jsonify(get_allowed_plugin_display_list())

@app.route('/plugin_info_field_type', methods=['POST'])
def get_plugin_info_def():
    plugin_name = request.form.get('plugin_name')

    if plugin_name not in get_allowed_plugin_list():
        return abort(400, 'Plugin not allowed!')

    result = dispatch_plugin("info_def", plugin_name)
    if (isinstance(result, tuple) and result[0] == PluginReturnStatus.SUCCESS):
        info = result[1]
        return jsonify(info)
    else:
        return abort(400, 'Plugin info_def function failed!')

@app.route('/PI_info_value', methods=['POST'])
def get_plugin_instance_info_value():
    plugin_instance_id = request.form.get('id')
    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is None:
        abort(400, 'No such plugin instance!')

    plugin_name = plugin_instance.plugin_name
    result = dispatch_plugin("info_def", plugin_name)
    if (isinstance(result, tuple) and result[0] == PluginReturnStatus.SUCCESS):
        plugin_info_def = result[1]
        logging.debug("info_value: %s", plugin_instance.plugin_init_info)
        info_value_list =  json.loads(plugin_instance.plugin_init_info)
        info={\
            "hint":plugin_info_def["hint"], \
            "source_name":plugin_instance.source_name, \
            "interval":plugin_instance.update_interval, \
            "info_value": plugin_info_def["field_def"],}
        for field in plugin_info_def["field_def"]:
            field["value"] = info_value_list[field["field_name"]]
        return jsonify(info)
    else:
        return abort(400, 'Plugin info_def function failed!')

if __name__ == '__main__':
    app.run()
