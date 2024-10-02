from datetime import datetime
from typing import Any, Dict, Generator

from lxml.etree import iterparse, Element


class XmlParser:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse_categories(self) -> Dict[str, Dict]:
        result: Dict[str, Dict] = {}
        for event, categories in iterparse(self.file_path, tag="categories"):
            for category in categories:
                category_id = category.get("id")
                category_parent_id = category.get("parentId")
                category_name = category.text
                result[category_id] = {
                    "name": category_name,
                    "parentId": category_parent_id,
                }
        return result

    def parse_offer(self, offer: Element) -> Dict[str, Any]:
        return {
            "marketplace_id": offer.findtext("marketplaceId"),
            "product_id": offer.get("id"),
            "title": offer.findtext("name"),
            "description": offer.findtext("description"),
            "brand": offer.findtext("vendor"),
            "seller_id": offer.findtext("seller_id"),
            "seller_name": offer.findtext("seller_name"),
            "first_image_url": offer.findtext("picture"),
            "category_id": offer.findtext("categoryId"),
            "features": offer.findtext("params"),
            "rating_count": offer.findtext("ratingCount"),
            "rating_value": offer.findtext("ratingValue"),
            "price_before_discount": offer.findtext("oldprice"),
            "discount": offer.findtext("discount"),
            "price_after_discount": offer.findtext("price"),
            "bonuses": offer.findtext("bonuses"),
            "sales": offer.findtext("sales"),
            "updated_at": datetime.fromtimestamp(int(offer.findtext("modified_time"))),
            "currency": offer.findtext("currencyId"),
            "barcode": offer.findtext("barcode"),
        }

    def parse_offers(self) -> Generator[Dict[str, Any], None, None]:
        for event, offers in iterparse(self.file_path, tag="offers"):
            for offer in offers:
                yield self.parse_offer(offer)
