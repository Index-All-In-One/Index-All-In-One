from flask import Flask, jsonify, request
import requests

def get_search_results(opensearch_conn, request, include_fields=None):
    keywords = request.form.get('keywords')
    full_text_keywords = request.form.get('full_text_keywords')
    # Connect with openSearch
    response = opensearch_conn.search_doc(keywords,full_text_keywords, include_fields=include_fields)
    return response

def extract_docs_from_response(response):
    docs = []
    for hit in response['hits']['hits']:
        docs.append(hit['_source'])
    return docs

def get_search_count(opensearch_conn, request):
    response = get_search_results(opensearch_conn, request, include_fields=None)
    return response['hits']['total']['value']

def exchange_auth_code(auth_code, redirect_uri, gdrive_client_id, gdrive_client_secret):
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": auth_code,
        "client_id": gdrive_client_id,
        "client_secret": gdrive_client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    response = requests.post(url, data=payload)
    return response.json()
