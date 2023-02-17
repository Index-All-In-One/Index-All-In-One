from opensearchpy import OpenSearch

# Set the API endpoint URL
# Set the search query and any required headers or parameters
# Set the authentication credentials
client = OpenSearch(
    hosts = [{"host": "localhost", "port": 9200}],
    http_auth = ("admin", "admin"),
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
)
client.info()

response = client.search(
    index="fruits",
    body={
        "query": {
            "match": {
                "name": "kiwi"
            }
        }          
    }
)
# Get the response content
print(response)
print(type(response))