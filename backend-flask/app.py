from flask import Flask, jsonify, request
from search_funcs import *

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

@app.route('/delete/source', methods=['POST'])
def delete_by_source():

    # keywords is a list of strings
    keywords = request.form.get('keywords').split(' ')

    # Connect with openSearch
    client = connect_OpenSearch()
    response = delete_source(client, keywords)
    docs = response['hits']['hits']
    return None


if __name__ == '__main__':
    app.run()