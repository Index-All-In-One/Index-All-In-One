from flask import Flask, jsonify, request, abort
import uuid
import logging
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from model_flask import *
from plugins.entry_plugin import dispatch_plugin
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

    # keywords is a list of strings
    keywords = request.form.get('keywords').split(' ')

    # Connect with openSearch
    response = opensearch_conn.search_doc(keywords)
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
    json_data = request.get_json()

    try:
        plugin_name = json_data['plugin_name']
        source_name = json_data['source_name']
        interval = json_data['interval']
        plugin_init_info = json_data['plugin_init_info']

    except KeyError:
        if plugin_name is None:
            abort(400, 'Missing key: plugin_name')
        if source_name is None:
            abort(400, 'Missing key: source_name')
        if interval is None:
            abort(400, 'Missing key: interval')
        if plugin_init_info is None:
            abort(400, 'Missing key: plugin_init_info')

    # plugin_init_info = json.loads(plugin_init_info)
    plugin_instance_id=str(uuid.uuid4())
    new_plugin_instance = PluginInstance(plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, source_name=source_name, update_interval=interval, enabled=True, active=False)
    sqlalchemy_db.session.add(new_plugin_instance)
    sqlalchemy_db.session.commit()

    # TODO: handle plugin init failure
    # TODO: add log support for plugin init
    status = dispatch_plugin("plugin_management.", "init", plugin_name, [plugin_instance_id, plugin_init_info])
    app.logger.debug("Plugin instance init: %s, %s, %s", plugin_name, plugin_instance_id, str(plugin_init_info))

    new_request = Request(request_op="activate", plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, update_interval=interval)
    sqlalchemy_db.session.add(new_request)
    sqlalchemy_db.session.commit()

    return 'Add plugin instance successfully!'

@app.route('/del_PI', methods=['POST'])
def delete_plugin_instance():
    plugin_instance_id = request.form.get('id')

    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is not None:
        plugin_name = plugin_instance.plugin_name
        sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).delete()
        sqlalchemy_db.session.commit()

        dispatch_plugin("plugin_management.", "del", plugin_name, [plugin_instance_id])
        app.logger.debug("Plugin instance del: %s, %s", plugin_name, plugin_instance_id)

        new_request = Request(request_op="deactivate", plugin_instance_id=plugin_instance_id)
        sqlalchemy_db.session.add(new_request)
        sqlalchemy_db.session.commit()
    else:
        return 'No such plugin instance!'

    return 'Delete plugin instance successfully!'

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
            })
    return jsonify(all_accounts)

if __name__ == '__main__':
    app.run()
