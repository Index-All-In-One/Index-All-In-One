from flask import Flask, jsonify, request, abort
from search_funcs import *
from plugin_management.model_flask import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PI.db'
sqlalchemy_db.init_app(app)
with app.app_context():
    sqlalchemy_db.create_all()


@app.route('/')
def hello():
    return 'Welcome!'

@app.route('/test')
def api():
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
def submit():

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

@app.route('/add_PI', methods=['GET'])
def add_plugin_instance():
    name = request.args.get('name')
    interval = request.args.get('interval')

    if name is None:
        abort(400, 'Missing required parameter: name')
    if interval is None:
        abort(400, 'Missing required parameter: interval')

    new_request = Request(request_op="add", plugin_name=name, update_interval=interval)
    sqlalchemy_db.session.add(new_request)
    sqlalchemy_db.session.commit()


    return 'Add plugin instance successfully!'

@app.route('/del_PI', methods=['GET'])
def delete_plugin_instance():
    id = request.args.get('id')

    if id is None :
        abort(400, 'Missing required parameter: id')

    new_request = Request(request_op="del", plugin_instance_id=id)
    sqlalchemy_db.session.add(new_request)
    sqlalchemy_db.session.commit()

    return 'Delete plugin instance successfully!'

if __name__ == '__main__':

    app.run()
