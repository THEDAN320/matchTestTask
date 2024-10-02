from typing import List, Dict, Any, Optional

from elasticsearch import helpers

from app.configs.elasticsearch import get_client
from .indexer import Indexer


class ElasticMatcher:
    def __init__(self):
        self.client = get_client()
        self.index = "goods"
        self.indexer = Indexer()

    def indexing(self, data: List[Dict[str, Any]]) -> None:
        indices = self.indexer.indexing(self.index, data)
        helpers.bulk(self.client, indices)

    def matching(self, data) -> Optional[List[str]]:
        ...

    def delete_index(self) -> None:
        self.client.indices.delete(index=self.index)
