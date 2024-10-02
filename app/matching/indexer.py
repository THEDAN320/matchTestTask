from typing import List, Dict, Any


class Indexer:
    def preparing_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "uuid": data.get("uuid"),
            "title": data.get("title"),
            "description": data.get("description"),
            "brand": data.get("brand"),
            "category": data.get("category_lvl_3") or data.get("category_lvl_2") or data.get("category_lvl_1")
        }

    def indexing(self, index: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [
            {"_index": index, "_id": item.get("uuid"), "_source": self.preparing_data(item)} for item in data
        ]
