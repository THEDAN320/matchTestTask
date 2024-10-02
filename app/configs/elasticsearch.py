from app.configs.connections import ELASTIC_HOST, ELASTIC_PORT

from elasticsearch import Elasticsearch


CONNECTION_URL = f"http://{ELASTIC_HOST}:{ELASTIC_PORT}"


def get_client() -> Elasticsearch:
    return Elasticsearch(CONNECTION_URL)
