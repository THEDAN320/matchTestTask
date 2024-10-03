from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column, UUID, INTEGER, BIGINT, TIMESTAMP, TEXT, JSON, DOUBLE_PRECISION, REAL, ARRAY, Index, func
)


class Base(DeclarativeBase):
    pass


class Sku(Base):
    __tablename__ = "sku"
    __table_args__ = (
        Index("sku_brand_index", "brand"),
        Index("sku_marketplace_id_sku_id_uindex", "marketplace_id", "product_id", unique=True),
        Index("sku_uuid_uindex", "uuid", unique=True),

    )

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, comment="id товара в нашей бд")
    marketplace_id = Column(INTEGER, nullable=True, comment="id маркетплейса")
    product_id = Column(BIGINT, nullable=True, comment="id товара в маркетплейсе")
    title = Column(TEXT, nullable=True, comment="название товара")
    description = Column(TEXT, nullable=True, comment="описание товара")
    brand = Column(TEXT, nullable=True)
    seller_id = Column(INTEGER, nullable=True)
    seller_name = Column(TEXT, nullable=True)
    first_image_url = Column(TEXT, nullable=True)
    category_id = Column(INTEGER, nullable=True)
    category_lvl_1 = Column(TEXT, nullable=True, comment="Первая часть категории товара")
    category_lvl_2 = Column(TEXT, nullable=True, comment="Вторая часть категории товара")
    category_lvl_3 = Column(TEXT, nullable=True, comment="Третья часть категории товара")
    category_remaining = Column(TEXT, nullable=True, comment="Остаток категории товара")
    features = Column(JSON, nullable=True, comment="Характеристики товара")
    rating_count = Column(INTEGER, nullable=True, comment="Кол-во отзывов о товаре")
    rating_value = Column(DOUBLE_PRECISION, nullable=True, comment="Рейтинг товара (0-5)")
    price_before_discount = Column(REAL, nullable=True)
    discount = Column(DOUBLE_PRECISION, nullable=True)
    price_after_discount = Column(REAL, nullable=True)
    bonuses = Column(INTEGER, nullable=True)
    sales = Column(INTEGER, nullable=True)
    inserted_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True)
    currency = Column(TEXT, nullable=True)
    barcode = Column(BIGINT, nullable=True, comment="Штрихкод")
    similar_sku = Column(ARRAY(UUID(as_uuid=True)), nullable=True)  # type: ignore

    def read(self):
        return {
            "uuid": self.uuid,
            "marketplace_id": self.marketplace_id,
            "product_id": self.product_id,
            "title": self.title,
            "description": self.description,
            "brand": self.brand,
            "seller_id": self.seller_id,
            "seller_name": self.seller_name,
            "first_image_url": self.first_image_url,
            "category_id": self.category_id,
            "category_lvl_1": self.category_lvl_1,
            "category_lvl_2": self.category_lvl_2,
            "category_lvl_3": self.category_lvl_3,
            "category_remaining": self.category_remaining,
            "features": self.features,
            "rating_count": self.rating_count,
            "rating_value": self.rating_value,
            "price_before_discount": self.price_before_discount,
            "discount": self.discount,
            "price_after_discount": self.price_after_discount,
            "bonuses": self.bonuses,
            "sales": self.sales,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
            "currency": self.currency,
            "barcode": self.barcode,
            "similar_sku": self.similar_sku,
        }
