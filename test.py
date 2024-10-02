from elasticsearch import Elasticsearch

client = Elasticsearch("http://elasticsearch:9200")
print(client.connector)