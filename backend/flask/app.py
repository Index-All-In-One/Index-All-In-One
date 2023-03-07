from flask import Flask, jsonify, request, abort
import uuid
import logging
import json
import os
import sys, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model_flask import *
from plugins.entry_plugin import dispatch_plugin, get_allowed_plugin_list
from plugins.status_code import PluginReturnStatus
from opensearch.conn import OpenSearch_Conn


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

@app.route('/search', methods=['POST'])
def search():

    # turn keywords into a list of dict
    keywords = request.form.get('keywords')
    full_text_keywords = request.form.get('full_text_keywords')
    # Connect with openSearch
    response = opensearch_conn.search_doc(keywords,full_text_keywords)
    docs = response['hits']['hits']

    search_results = []
    for doc in docs:
        doc = doc['_source']
        search_results.append(
            {
                "doc_name": doc['doc_name'],
                "doc_type": doc['doc_type'],
                "link": doc['link'],
                "source": doc['source'],
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
        abort(400, 'Missing key: plugin_name')
    if source_name is None:
        abort(400, 'Missing key: source_name')
    if interval is None:
        abort(400, 'Missing key: interval')
    if plugin_init_info is None:
        abort(400, 'Missing key: plugin_init_info')

    if plugin_instance_id is not None:
        plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
        if plugin_instance is not None:
            return abort(400, 'Plugin instance already exists!')
    else:
        plugin_instance_id=str(uuid.uuid4())

    new_plugin_instance = PluginInstance(plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, source_name=source_name, update_interval=interval, enabled=True, active=False)
    sqlalchemy_db.session.add(new_plugin_instance)
    sqlalchemy_db.session.commit()

    # TODO: return status code for plugin init failure,
    # TODO: add log support inside plugin init

    try:
        status = dispatch_plugin("init", plugin_name, [plugin_instance_id, plugin_init_info])
    except Exception as e:
        app.logger.error(e)
        status = PluginReturnStatus.EXCEPTION

    if status == PluginReturnStatus.SUCCESS:
        new_request = Request(request_op="activate", plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, update_interval=interval)
        sqlalchemy_db.session.add(new_request)
        sqlalchemy_db.session.commit()

        app.logger.debug("Plugin instance init Success! : %s, %s, %s", plugin_name, plugin_instance_id, str(plugin_init_info))
        return 'Add plugin instance successfully!'
    else:
        # TODO: handle plugin init failure
        app.logger.error("Plugin instance init failed! Status: %d : %s, %s, %s", status.name, plugin_name, plugin_instance_id, str(plugin_init_info))
        return 'Plugin instance init function failed!'

@app.route('/del_PI', methods=['POST'])
def delete_plugin_instance():
    plugin_instance_id = request.form.get('id')

    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is None:
        return 'No such plugin instance!'

    plugin_name = plugin_instance.plugin_name
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

    time.sleep(8)
    response = opensearch_conn.delete_doc(plugin_instance_id=plugin_instance_id)
    app.logger.debug("plugin_instance_id %s delete_doc: %s", plugin_instance_id, response)

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
    return jsonify(get_allowed_plugin_list())

@app.route('/plugin_info_field_type', methods=['POST'])
def get_plugin_info_list():
    plugin_name = request.form.get('plugin_name')
    status, info = dispatch_plugin("info_list", plugin_name)
    return jsonify(info)

if __name__ == '__main__':
    app.run()
