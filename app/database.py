from typing import Any, Dict
from app.repositories import SkuRepository


class DataBase:
    def __init__(self) -> None:
        self.sku_repository = SkuRepository()

    def add(self, data: Dict[str, Any]) -> None:
        self.sku_repository.add(data)
