from flask import Flask, jsonify, request
from opensearchpy import OpenSearch
import pandas as pd
from datetime import datetime

INDEX_NAME = 'search_index'

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

    def connect_OpenSearch():
        client = OpenSearch(
        hosts = [{"host": "localhost", "port": 9200}],
        http_auth = ("admin", "admin"),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        )
        return client

    def search_OpenSearch(client, keywords=None):
        if not keywords or len(keywords) == 0:
            response = client.search(
                index=INDEX_NAME,
                body={
                    "query": {
                        "match_all": {}
                    }
                }
            )
        # with a list of keywords, search for documents that match either of the keywords in the list.
        else:
            response = client.search(
                index=INDEX_NAME,
                body={
                    "query": {
                        "bool": {
                            "should": [
                                {"match": {"doc_name": keyword}} for keyword in keywords
                            ]
                        }
                    }
                }
            )
        return response

    # keywords is a list of strings
    keywords = request.form.get('keywords').split(' ')

    client = connect_OpenSearch()
    # print(client.info())
    response = search_OpenSearch(client, keywords)
    # print(response)

    docs = response['hits']['hits']
    # print(docs)
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

if __name__ == '__main__':
    app.run()