from uuid import uuid4
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column, UUID, INTEGER, BIGINT, TIMESTAMP, TEXT, JSON, DOUBLE_PRECISION, REAL, ARRAY, Index, func
)


class Sku(DeclarativeBase):
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
