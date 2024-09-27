from app.parser import XmlParser, CategoryManager
from app.utils import get_files_list, get_file_path


def file_processing(file_path: str):
    parser = XmlParser(file_path)
    categories = parser.parse_categories()
    category_manager = CategoryManager(categories)
    for offer_data in parser.parse_offers():
        category_id = offer_data.get("category_id")
        if category_id:
            lvls = category_manager.get_categories_lvl(category_id)
            offer_data.update(lvls)
        


if __name__ == "__main__":
    files = get_files_list()
    for file in files:
        file_path = get_file_path(file)
        file_processing(file_path)
