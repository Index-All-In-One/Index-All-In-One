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
    '''
    with a list of keywords, search for documents that match either of the keywords in the list.
    Input: 
        client: a connectd OpenSearch client
        keywords: the search keyword
        index_name: the name of an OpenSearch index
    Output:
        the search response in the form of a python dict
    '''
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

def delete_OpenSearch(client, field_values: dict, index_name='search_index'):
    '''
    Delete OpenSource client documents
    Sample Usage: delete documents from source source1 with doc_id 1: delete_OpenSearch(client, {"source": source1, "doc_id": 1})

    Input: 
        client: a connectd OpenSearch client
        field_values: the delete field: value pairs
        index_name: the name of an OpenSearch index
    Output:
        the delete result
    '''

    body = {
        "query": {
            "match": field_values
        }
    }
    response = client.delete_by_query(index=index_name, body=body)
    return response