from typing import List, Dict, Any, Generator

from elasticsearch import helpers

from app.configs.elasticsearch import get_client
from .indexer import Indexer


class ElasticMatcher:
    def __init__(self, index: str):
        self.index = index
        self.client = get_client()
        self.indexer = Indexer()

    def indexing(self, data: Generator[Dict[str, Any], None, None]) -> None:
        indices = self.indexer.indexing(self.index, data)
        helpers.bulk(self.client, indices)

    def match(self, data: Dict[str, Any]) -> List[str]:
        match_data = self.client.search(
            index=self.index,
            query={
                "bool": {
                    "must": [
                        {"match": {"brand": data.get("brand")}},
                        {"match": {"category": data.get("category_lvl_3") or data.get("category_lvl_2") or data.get("category_lvl_1")}},
                    ]
                }
            },
            size=5,
        )
        results: list[str] = []
        if match_data["hits"]["total"]["value"] > 0:
            data_uuid = str(data["uuid"])
            for hit in match_data["hits"]["hits"]:
                if data_uuid != hit["_id"]:
                    results.append(hit["_id"])
        return results
