from typing import Dict, List, Optional


class CategoryManager:
    def __init__(self, categories: Dict[str, Dict]) -> None:
        self.categories = categories
        self.categories_lvls = [
            "category_lvl_1",
            "category_lvl_2",
            "category_lvl_3",
            "category_remaining"
        ]

    def get_parent(self, category_id: str) -> Optional[str]:
        category = self.categories.get(category_id)
        if category is None:
            return None
        return category.get("parentId")

    def get_name_by_id(self, category_id: str) -> Optional[str]:
        category = self.categories.get(category_id)
        if category is None:
            return None
        return category.get("name")

    def get_categories_tree(self, category_id: str) -> List[str]:
        current_id = category_id
        categories_id = [current_id]
        while parent_id := self.get_parent(current_id):
            categories_id.append(parent_id)
            current_id = parent_id
        return categories_id

    def _to_dict(self, categories_name: list[str]) -> Dict[str, str]:
        count = 0
        result: Dict[str, str] = {}
        for lvl in categories_name:
            lvl_name = self.categories_lvls[count]
            result[lvl_name] = lvl
            count += 1
        return result

    def get_categories_lvl(self, category_id: str) -> Dict[str, str]:
        categories_tree = self.get_categories_tree(category_id)
        temp_categories_name = []
        for category_id in categories_tree:
            name = self.get_name_by_id(category_id)
            if name:
                temp_categories_name.append(name)
        temp_categories_name.reverse()
        categories_name = []
        if len(temp_categories_name) > 3:
            categories_name.append(temp_categories_name[0])
            categories_name.append(temp_categories_name[1])
            categories_name.append(temp_categories_name[2])
            category_remaining = "/".join(temp_categories_name[3:])
            categories_name.append(category_remaining)
        else:
            categories_name = temp_categories_name
        return self._to_dict(categories_name)

    def get_category_info(self, category_id: str) -> Dict[str, str]:
        result = {
            "category_id": category_id
        }
        category_lvls = self.get_categories_lvl(category_id)
        return result | category_lvls
