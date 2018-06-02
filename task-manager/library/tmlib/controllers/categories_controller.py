from tmlib.storage.category_storage import CategoryStorage
from tmlib.controllers.base_controller import BaseController


def create_categories_controller(user_id, database_name):
    return CategoriesController(user_id, CategoryStorage(database_name))


class CategoriesController(BaseController):
    """Class for managing categories"""

    def create(self, category):
        category.user_id = self.user_id
        return self.storage.create(category)

    def update(self, category):
        return self.storage.update(category)

    def delete(self, category_id):
        self.storage.delete_by_id(category_id)

    def get_by_id(self, category_id):
        return self.storage.get_by_id(category_id)

    def all(self):
        return self.storage.all_user_categories(self.user_id)
