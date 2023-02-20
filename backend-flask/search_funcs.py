from opensearchpy import OpenSearch

def connect_OpenSearch(host='localhost', port=9200, username='admin', password='admin', 
use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

    client = OpenSearch(
    hosts = [{"host": host, "port": port}],
    http_auth = (username, password),
    use_ssl = use_ssl,
    verify_certs = verify_certs,
    ssl_assert_hostname = ssl_assert_hostname,
    ssl_show_warn = ssl_show_warn,
    )
    return client

def search_OpenSearch(client, keywords, index_name='search_index'):
    # with a list of keywords, search for documents that match either of the keywords in the list.
    response = client.search(
        index=index_name,
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

def delete_source(client, keywords, index_name='search_index'):
    response = client.delete_by_query(
        index=index_name,
        body={
            "query": {
                "bool": {
                    "should": [
                        {"match": {"source": keyword}} for keyword in keywords
                    ]
                }
            }
        }
    )
    return response

def delete_by_id(client, id, index_name='search_index'):
    # response = client.delete(index=index_name, doc_id=id, refresh=True, q="your_keyword")
    return response
