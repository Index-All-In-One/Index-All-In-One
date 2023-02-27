from flask import Flask, jsonify, request, abort
import uuid
from search_funcs import *
from plugin_management.model_flask import *
from plugin_management.plugins.plugin_entry import dispatch_plugin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PI.db'
sqlalchemy_db.init_app(app)
with app.app_context():
    sqlalchemy_db.create_all()


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
    client = connect_OpenSearch()
    response = search_OpenSearch(client, keywords)
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
    plugin_name = request.form.get('plugin_name')
    source_name = request.form.get('source_name')
    interval = request.form.get('interval')
    plugin_init_info = request.form.get('plugin_init_info')

    if plugin_name is None:
        abort(400, 'Missing required parameter: plugin_name')
    if source_name is None:
        abort(400, 'Missing required parameter: source_name')
    if interval is None:
        abort(400, 'Missing required parameter: interval')
    if plugin_init_info is None:
        abort(400, 'Missing required parameter: plugin_init_info')

    plugin_instance_id=str(uuid.uuid4())
    new_plugin_instance = PluginInstance(plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, source_name=source_name, update_interval=interval, enabled=True, active=False)
    sqlalchemy_db.session.add(new_plugin_instance)
    sqlalchemy_db.session.commit()

    # TODO: handle plugin init failure
    status = dispatch_plugin("plugin_management.", "init", plugin_name, [plugin_instance_id, plugin_init_info])

    new_request = Request(request_op="activate", plugin_name=plugin_name, plugin_instance_id=plugin_instance_id, update_interval=interval)
    sqlalchemy_db.session.add(new_request)
    sqlalchemy_db.session.commit()

    return 'Add plugin instance successfully!'

@app.route('/del_PI', methods=['GET'])
def delete_plugin_instance():
    plugin_instance_id = request.args.get('id')

    if plugin_instance_id is None :
        abort(400, 'Missing required parameter: id')

    plugin_instance = sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).first()
    if plugin_instance is not None:
        plugin_name = plugin_instance.plugin_name
        sqlalchemy_db.session.query(PluginInstance).filter(PluginInstance.plugin_instance_id == plugin_instance_id).delete()
        sqlalchemy_db.session.commit()

        dispatch_plugin("plugin_management.", "del", plugin_name, [plugin_instance_id])

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
