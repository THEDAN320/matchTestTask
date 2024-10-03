from collections.abc import Generator
from typing import Any
from uuid import UUID

from app.repositories import SkuRepository


class SKUService:
    def __init__(self) -> None:
        self.sku_repository = SkuRepository()

    def add(self, data: dict[str, Any]) -> None:
        self.sku_repository.add(data)

    def update(self, uuid: UUID, data: dict[str, Any]) -> None:
        self.sku_repository.update(uuid, data)

    def get_all(self, filter_by: dict) -> Generator[dict[str, Any], None, None]:
        return self.sku_repository.get_all(filter_by)

    def get_range(
        self, offset: int = 0, count: int = 1000
    ) -> Generator[dict[str, Any], None, None]:
        return self.sku_repository.get_range(offset, count)
