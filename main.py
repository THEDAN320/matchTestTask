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


def file_processing(file_path: str, service: SKUService):
    logger.info("Парсинг категорий...")
    parser = XmlParser(file_path)
    categories = parser.parse_categories()
    category_manager = CategoryManager(categories)

    logger.info("Парсинг товаров...")
    count = 0
    for offer_data in parser.parse_offers():
        category_id = offer_data.get("category_id")
        if category_id:
            lvls = category_manager.get_categories_lvl(category_id)
            offer_data.update(lvls)
        service.add(offer_data)

        count += 1
        if count % 2000 == 0:
            logger.info(f"Добавлено {count} товаров...")

    logger.info("Все товары добавлены!")


def indexing(matcher: ElasticMatcher, service: SKUService) -> None:
    logger.info("Загрузка товаров для индексации...")
    data = service.get_all({})
    matcher.indexing(data)
    logger.info("Товары загружены!")


def matching(matcher: ElasticMatcher, service: SKUService) -> None:
    logger.info("Поиск похожих товаров...")
    for good in service.get_all({}):
        matches = matcher.match(good)
        if matches:
            service.update(good["uuid"], {"similar_sku": matches})
    logger.info("Поиск закончен!")


def main():
    service = SKUService()

    logger.info("Получение файлов...")
    files = get_files_list()

    logger.info(f"Обнаружено aайлов: {len(files)}.")
    for file in files:
        logger.info(f"Обработка файла: {file}...")
        file_path = get_file_path(file)
        file_processing(file_path, service)

    index = "goods"
    matcher = ElasticMatcher(index)
    indexing(matcher, service)
    matching(matcher, service)


if __name__ == "__main__":
    logger.info("Создание таблиц...")
    Base.metadata.create_all(engine)
    logger.info("Запуск скрипта...")
    main()
    logger.info("Конец скрипта.")
