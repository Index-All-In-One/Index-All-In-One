from opensearchpy import OpenSearch

class OpenSearch_Conn:
    def __init__(self):
        self.client = None

    def connect(self, host='localhost', port=9200, username='admin', password='admin', 
    use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

        self.client = OpenSearch(
        hosts = [{"host": host, "port": port}],
        http_auth = (username, password),
        use_ssl = use_ssl,
        verify_certs = verify_certs,
        ssl_assert_hostname = ssl_assert_hostname,
        ssl_show_warn = ssl_show_warn,
        )
        return self.client

    def insert_index(self, body:dict, index_name='search_index'):
        response = self.client.indices.create(index=index_name,body=body)
        return response

    def insert_doc(self, body: dict, index_name='search_index'):
        response = self.client.index(index=index_name,body=body)
        return response

    def search_doc(self, keywords, index_name='search_index'):
        '''
        with a list of keywords, search for documents that match either of the keywords in the list.
        Input: 
            client: a connectd OpenSearch client
            keywords: the search keyword
            index_name: the name of an OpenSearch index
        Output:
            the search response in the form of a python dict
        '''
        response = self.client.search(
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

    def delete_doc(self, keywords: dict, index_name='search_index'):
        '''
        Delete OpenSource client documents
        Sample Usage: delete documents from source source1 with doc_id 1: delete_OpenSearch(client, {"source": source1, "doc_id": 1})

        Input: 
            client: a connectd OpenSearch client
            fields: the delete field: value pairs
            index_name: the name of an OpenSearch index
        Output:
            the delete result
        '''

        body = {
            "query": {
                "bool": {
                    "must": keywords
                } 
            }
        }
        response = self.client.delete_by_query(index=index_name, body=body)
        return response

    def delete_index(self, index_name):
        response = self.client.indices.delete(index=index_name)
        return response

    def get_doc_count(self, index_name='search_index'):
        response = self.client.count(index=index_name)
        return response

    def get_doc_ids(self, source, index_name='search_index'):
        body = {
            "query": {
                "match_all": {}
            },
            "_source": ["doc_id"]
        }
        results = self.client.search(index=index_name, body=body)
        doc_ids = [hit["_source"]["doc_id"] for hit in results["hits"]["hits"]]
        # print(doc_ids)
        return doc_ids



def dummy_data():
    from datetime import datetime
    doc_id = 1
    doc_name = "Google"
    doc_type = "txt"
    link = "https://www.google.com/"
    source = "Gmail"
    created_date = datetime(2022, 2, 18, 12, 30, 0).strftime('%Y-%m-%dT%H:%M:%SZ')
    modified_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    summary = "Google is a multinational technology company that specializes in Internet-related services and products. It was founded in 1998 by Larry Page and Sergey Brin, who were graduate students at Stanford University at the time. Today, Google is one of the largest and most influential companies in the world, with a market capitalization of over $1 trillion."
    file_size = len(summary.encode('utf-8'))
    
    body = {
        "doc_id": doc_id,
        "doc_name": doc_name,
        "doc_type": doc_type,
        "link": link,
        "source": source,
        "created_date": created_date,
        "modified_date": modified_date,
        "summary": summary,
        "file_size": file_size
    }
    return body

if __name__ == "__main__":
    import json
    index_name='search_index'
    conn = OpenSearch_Conn()
    conn.connect()
    conn.delete_index(index_name)
    data = json.load(open("index.json", 'r'))
    conn.insert_index(data)
