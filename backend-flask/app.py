from flask import Flask, jsonify, request
from opensearchpy import OpenSearch
import pandas as pd
from datetime import datetime

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
    async def connect_OpenSearch():
        client = await OpenSearch(
        hosts = [{"host": "localhost", "port": 9200}],
        http_auth = ("admin", "admin"),
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
        )
        return client

    async def search_OpenSearch(client):
        response = await client.search(
            index='search_index',
            body={
                "query": {
                    "match_all": {}
                }
            }
        )
        return response

    keywords = request.form.get('keywords')
    foo = request.form.get('foo')
    print(keywords)
    print(foo)

    client = connect_OpenSearch()
    print(client.info())
    response = search_OpenSearch(client)
    print(response)
    print()
    print()

    # docs = response['hits']['hits']
    search_results = []
    # for doc in docs:
    #     search_results.append(
    #         {
    #             "doc_name": doc['doc_name'],
    #             "doc_type": doc['doc_type'],
    #             "link": doc['link'],
    #             "source": doc['source'],
    #             "created_date": doc['created_date'],
    #             "modified_date": doc['modified_date'],
    #             "summary": doc['summary'],
    #             "file_size": doc['file_size']
    #         })

    return jsonify(search_results)

if __name__ == '__main__':
    app.run()