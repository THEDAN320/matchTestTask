from typing import Any, Dict
from uuid import UUID

from app.repositories import SkuRepository


class SKUService:
    def __init__(self) -> None:
        self.sku_repository = SkuRepository()

    def add(self, data: Dict[str, Any]) -> None:
        self.sku_repository.add(data)

    def update(self, uuid: UUID, data: Dict[str, Any]) -> None:
        self.sku_repository.update(uuid, data)

    def get_all(self, filter_by: dict) -> list[dict[str, Any]]:
        return self.sku_repository.get_all(filter_by)
