from opensearchpy import OpenSearch
import json
class OpenSearch_Conn:
    def __init__(self):
        self.client = None

    def connect(self, host='localhost', port=9200, username='admin', password='admin',
    use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):
        '''
            Connect to Opensearch Client
        '''
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
        '''
        Build index on Opensearch,
        Example:
            body = json.load(open("index.json", 'r'))
            OpenSearch_Conn.insert_index(body)
        '''
        try:
            response = self.client.indices.create(index=index_name,body=body)
        except:
            return False
        return True

    def insert_doc(self, body: dict, index_name='search_index'):
        '''
        Insert a document to index
        Example:
            body = {
                "doc_id": doc_id,
                "doc_name": doc_name,
                "doc_type": doc_type,
                "link": link,
                "source": source,
                "created_date": created_date,
                "modified_date": modified_date,
                "summary": summary,
                "file_size": file_size,
                "plugin_instance_id": plugin_instance_id,
                "content": content
            }
            OpenSearch_Conn.insert_doc(body)
        '''
        response = self.client.index(index=index_name,body=body)
        return response

    def search_doc(self, doc_name, full_text_keywords=None, index_name='search_index'):
        '''
        with a list of keywords, search for documents that match either of the keywords in the list.
        Input:
            client: a connectd OpenSearch client
            keywords: the search keyword
            index_name: the name of an OpenSearch index
        Output:
            the search response in the form of a python dict
        Example:
            keywords = "Youtube"
            full_text_keywords = "Apple"
        '''
        keywords = []
        if doc_name:
            keywords.append({"match": {"doc_name": doc_name}})
        if full_text_keywords:
            keywords.append({"match": {"content": full_text_keywords}})

        response = self.client.search(
            index=index_name,
            body={
                "query": {
                    "bool": {
                        "should": keywords
                    }
                }
            }
        )

        return response

    def delete_doc(self, doc_id=None, plugin_instance_id=None, index_name='search_index'):
        '''
        Delete OpenSource client documents
        Sample Usage: delete documents from source source1 with doc_id 1: delete_OpenSearch(client, )

        Input:
            client: a connectd OpenSearch client
            fields: the delete field: value pairs
            index_name: the name of an OpenSearch index
        Output:
            the delete result
        Example:
            keywords = [{"match": {"doc_id": doc_id}}]
            keywords = [{"match": {"source": source1}}, {"match": {"doc_id": doc_id}}]
            OpenSearch_Conn.delete_doc(keywords)
        '''
        keywords = []
        if doc_id:
            keywords.append({"match": {"doc_id": doc_id}})
        if plugin_instance_id:
            keywords.append({"match": {"plugin_instance_id": plugin_instance_id}})

        if len(keywords)==0:
            return
        
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
        '''
        Delete the index and all documents under it
        '''
        try:
            response = self.client.indices.delete(index=index_name)
        except:
            return False
        return True

    def get_doc_count(self, index_name='search_index'):
        '''
        Output:
            The total number of documents under index
        '''
        response = self.client.count(index=index_name)
        return response

    def get_doc_ids(self, source, index_name='search_index'):
        '''
        Find all doc_id with a source
        '''

        body = {
            "query": {
                "match": {
                    "source": source
                }
            },
            "_source": ["doc_id"]
        }
        results = self.client.search(index=index_name, body=body)
        doc_ids = [hit["_source"]["doc_id"] for hit in results["hits"]["hits"]]
        return doc_ids


def init_opensearch_db(indexfile_path: str, host='localhost', port=9200, username='admin', password='admin',
    use_ssl=True, verify_certs=False, ssl_assert_hostname=False, ssl_show_warn=False):

    '''
    indexfile_path = "index.json"
    '''
    conn = OpenSearch_Conn()
    conn.connect(host, port, username, password, use_ssl, verify_certs, ssl_assert_hostname, ssl_show_warn)
    data = json.load(open(indexfile_path, 'r'))
    conn.insert_index(data)

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
    plugin_instance_id = "1"
    content = "Google is a multinational technology company that specializes in Internet-related services and products. It was founded in 1998 by Larry Page and Sergey Brin, who were graduate students at Stanford University at the time. Today, Google is one of the largest and most influential companies in the world, with a market capitalization of over $1 trillion. Youtube was bought by Google."
    
    body = {
        "doc_id": doc_id,
        "doc_name": doc_name,
        "doc_type": doc_type,
        "link": link,
        "source": source,
        "created_date": created_date,
        "modified_date": modified_date,
        "summary": summary,
        "file_size": file_size,
            "plugin_instance_id": plugin_instance_id,
            "content": content
    }
    return body

if __name__ == "__main__":
    index_name='search_index'
    conn = OpenSearch_Conn()
    conn.connect()
    status = conn.delete_index(index_name)
    print(status)
    data = json.load(open("opensearch/index.json", 'r'))
    status = conn.insert_index(data)
    print(status)

    # body = dummy_data()
    # conn.insert_doc(body)
    # response = conn.search_doc("Google", "Google")
    # print(response)
    # response = conn.get_doc_count()
    # print(response)
    # conn.delete_doc([{"match": {"plugin_instance_id": '1'}}])
    # response = conn.get_doc_count()
    # print(response)