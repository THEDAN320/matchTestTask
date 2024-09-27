from app.repositories.base import Repository

from app.models import Sku


class SkuRepository(Repository):
    model = Sku
