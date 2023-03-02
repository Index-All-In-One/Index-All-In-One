import sys
import os
import logging
from opensearch_conn import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == "__main__":
    index_file = "index.json"
    host = os.environ.get('OPENSEARCH_HOSTNAME', 'localhost')
    if len(sys.argv) >= 2:
        index_file = sys.argv[1]
    init_opensearch_db(index_file,host)
    logging.info("Index file %s is loaded into OpenSearch", index_file)
