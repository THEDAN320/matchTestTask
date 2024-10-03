import logging

from elasticsearch import Elasticsearch

from app.configs.database import engine
from app.matching import ElasticMatcher
from app.models import Base
from app.parser import XmlParser, CategoryManager
from app.services import SKUService
from app.utils import get_files_list, get_file_path


client = Elasticsearch("http://localhost:9200/", api_key="YOUR_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def file_processing(file_path: str):
    parser = XmlParser(file_path)
    service = SKUService()

    logger.info("Парсинг категорий...")
    categories = parser.parse_categories()
    category_manager = CategoryManager(categories)

    logger.info("Парсинг товаров...")
    count = 0
    for offer_data in parser.parse_offers():
        count += 1
        if count == 1000:
            break
        logger.info(count)
        category_id = offer_data.get("category_id")
        if category_id:
            lvls = category_manager.get_categories_lvl(category_id)
            offer_data.update(lvls)
        service.add(offer_data)

    logger.info("Загрузка товаров для индексации...")
    matcher = ElasticMatcher("goods")
    good = list(service.get_range())[0]
    print(matcher.matching(good))


if __name__ == "__main__":
    logger.info("Создание таблиц...")
    Base.metadata.create_all(engine)

    logger.info("Получение файлов...")
    files = get_files_list()

    logger.info(f"Обнаружено {len(files)} файлов.")
    for file in files:
        logger.info(f"Обработка файла: {file}...")
        file_path = get_file_path(file)
        file_processing(file_path)

    logger.info("Все файлы обработаны.")
