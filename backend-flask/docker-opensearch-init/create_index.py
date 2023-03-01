from opensearchpy import OpenSearch
import sys
import ssl

hostname = "localhost"
if len(sys.argv) >= 2:
    hostname = sys.argv[1]

# Connect to the OpenSearch node
ssl_context = ssl.create_default_context()
client = OpenSearch(
    hosts=[hostname],
    port=9200,
    use_ssl=True,
    ssl_context=ssl_context,
    http_compress=True
)

# Define the settings for the new index
settings = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        }
    }
}

# Create the index with the specified settings
response = client.indices.create(index="search_index", body=settings)

# Print the response from the OpenSearch node
print(response)
