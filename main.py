import logging

from elasticsearch import Elasticsearch

from app.configs.database import engine
from app.models import Base
from app.parser import XmlParser, CategoryManager
from app.services import SKUService
from app.utils import get_files_list, get_file_path


client = Elasticsearch("http://localhost:9200/", api_key="YOUR_API_KEY")

logger = logging.getLogger(__name__)


def file_processing(file_path: str):
    parser = XmlParser(file_path)
    logger.info("Парсинг категорий...")
    categories = parser.parse_categories()
    category_manager = CategoryManager(categories)
    service = SKUService()
    logger.info("Парсинг товаров...")
    for offer_data in parser.parse_offers():
        category_id = offer_data.get("category_id")
        if category_id:
            lvls = category_manager.get_categories_lvl(category_id)
            offer_data.update(lvls)
        service.add(offer_data)


if __name__ == "__main__":
    logger.info("Создание таблиц...")
    if 0:
        Base.metadata.create_all(engine)
        logger.info("Получение файлов...")
        files = get_files_list()
        logger.info(f"Обнаружено {len(files)} файлов.")
        for file in files:
            logger.info(f"Обработка файла: {file}...")
            file_path = get_file_path(file)
            file_processing(file_path)
        logger.info("Все файлы обработаны.")
