import sys
import os
import logging
import time
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from opensearch.conn import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == "__main__":
    index_file = "index.json"
    host = os.environ.get('OPENSEARCH_HOSTNAME', 'localhost')
    sleep_interval = 5
    if len(sys.argv) >= 2:
        index_file = sys.argv[1]
    if len(sys.argv) >= 3:
        sleep_interval = (int)(sys.argv[2])

    if check_index_exist(host=host):
        logging.info("Index already exists!")
        sys.exit(0)

    logging.info("Keep Trying Loading index file %s into OpenSearch", index_file)
    while True:
        try:
            init_opensearch_db(index_file,host)
        except Exception as e:
            logging.error("Failed to load index file %s into OpenSearch", index_file)
            logging.error(e)

        if check_index_exist(host=host):
            logging.info("Index file %s is loaded into OpenSearch", index_file)
            break

        time.sleep(sleep_interval)
