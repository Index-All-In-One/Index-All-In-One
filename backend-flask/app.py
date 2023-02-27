from flask import Flask, jsonify, request
from opensearch_conn import *
import json

opensearch_conn = OpenSearch_Conn()
opensearch_conn.connect()

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

    response = opensearch_conn.delete_doc(matches)
    return jsonify(response)

@app.route('/delete/index', methods=['POST'])
def delete_index():
    '''
    use case:
    curl -X POST -d "index_name=search_index" http://127.0.0.1:5000/delete/index
    '''

    index_name = request.form.get('index_name')
    response = opensearch_conn.delete_index(index_name)
    return jsonify(response)

@app.route('/insert/index', methods=['POST'])
def build_index():
    '''
    use case:
    curl -X POST -d "index_name=search_index" http://127.0.0.1:5000/insert/index
    '''

    index_name = request.form.get('index_name')
    data = json.load(open("index.json", 'r'))
    response = opensearch_conn.insert_index(data, index_name)
    return jsonify(response)

@app.route('/insert/doc', methods=['POST'])
def insert_doc():
    '''
    use case:
    curl -X POST http://127.0.0.1:5000/insert/doc
    '''
    # insert a dummy data

    keywords = dummy_data()
    response = opensearch_conn.insert_doc(keywords)
    return jsonify(response)

@app.route('/count', methods=['POST'])
def get_doc_count():
    '''
    use case:
    curl -X POST -d "index_name=search_index" http://127.0.0.1:5000/count
    '''

    index_name = request.form.get('index_name')
    response = opensearch_conn.get_doc_count(index_name)
    return jsonify(response)

if __name__ == '__main__':
    app.run()