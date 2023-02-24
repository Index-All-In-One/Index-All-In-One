from flask import Flask, jsonify, request
from opensearch_utils import *
import json
app = Flask(__name__)

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
    '''
    user case:
    curl -X POST -d "keywords=Google" http://127.0.0.1:5000/search
    '''
    # keywords is a list of strings
    keywords = request.form.get('keywords').split(' ')

    # Connect with openSearch
    client = connect_OpenSearch()
    response = search_doc_OpenSearch(client, keywords)
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

@app.route('/delete', methods=['POST'])
def delete_by_source():
    '''
    use case:
    curl -X POST -d 'keywords={"key1": "value1", "key2": "value2", ...}' http://127.0.0.1:5000/delete
    curl -X POST -d 'keywords={"doc_id": 1, "source": "Gmail"}' http://127.0.0.1:5000/delete
    '''

    # keywords is a list of strings
    keywords = json.loads(request.form.get('keywords'))
    matches = []
    for item in keywords.items():
        matches.append({"match": {item[0]: item[1]}})

    # Connect with openSearch
    client = connect_OpenSearch()
    response = delete_doc_OpenSearch(client, matches)
    return jsonify(response)

@app.route('/delete/index', methods=['POST'])
def delete_index():
    '''
    use case:
    curl -X POST -d "index_name=search_index" http://127.0.0.1:5000/delete/index
    '''
    client = connect_OpenSearch()
    index_name = request.form.get('index_name')
    response = delete_index_OpenSearch(client, index_name)
    return jsonify(response)

@app.route('/insert/index', methods=['POST'])
def build_index():
    '''
    use case:
    curl -X POST -d "index_name=search_index" http://127.0.0.1:5000/insert/index
    '''
    client = connect_OpenSearch()
    index_name = request.form.get('index_name')
    data = json.load(open("index.json", 'r'))
    response = insert_index_OpenSearch(client, data, index_name)
    return jsonify(response)

@app.route('/insert/doc', methods=['POST'])
def insert_doc():
    '''
    use case:
    curl -X POST http://127.0.0.1:5000/insert/doc
    '''
    # insert a dummy data
    client = connect_OpenSearch()
    keywords = dummy_data()
    response = insert_data_OpenSearch(client, keywords)
    return jsonify(response)

@app.route('/count', methods=['POST'])
def get_doc_count():
    '''
    use case:
    curl -X POST -d "index_name=search_index" http://127.0.0.1:5000/count
    '''
    client = connect_OpenSearch()
    index_name = request.form.get('index_name')
    response = get_doc_count_OpenSearch(client, index_name)
    return jsonify(response)


if __name__ == '__main__':
    app.run()