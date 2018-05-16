from storage.category_storage import CategoryStorage


class CategoriesController:
    def __init__(self, category_storage):
        self.category_storage = category_storage

    def create(self, category, user_id):
        category.user_id = user_id
        return self.category_storage.create(category)

    def update(self, category):
        return self.category_storage.update(category)

    def delete(self, category_id):
        self.category_storage.delete_by_id(category_id)

    def get_by_id(self, category_id):
        return self.category_storage.get_by_id(category_id)
