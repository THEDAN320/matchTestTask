from typing import List, Dict, Any, Optional

from elasticsearch import helpers

from app.configs.elasticsearch import get_client
from .indexer import Indexer


class ElasticMatcher:
    def __init__(self, index: str):
        self.index = index
        self.client = get_client()
        self.indexer = Indexer()

    def indexing(self, data: List[Dict[str, Any]]) -> None:
        indices = self.indexer.indexing(self.index, data)
        helpers.bulk(self.client, indices)

    def matching(self, data: Dict[str, Any]) -> Optional[List[str]]:
        match_products = self.client.search(
            index="products",
            query={
                "bool": {
                    "must": [
                        {"match": {"category_lvl_3": data["category_lvl_3"]}},
                        {"match": {"brand": data["brand"]}},
                    ]
                }
            },
            size=5,
        )

        if match_products["hits"]["total"]["value"] > 0:
            products = []
            for hit in match_products["hits"]["hits"]:
                products.append(hit["_source"])
            return products
        else:
            return None

    def delete_index(self) -> None:
        self.client.indices.delete(index=self.index)
