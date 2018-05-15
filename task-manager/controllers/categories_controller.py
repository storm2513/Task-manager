from storage.category_storage import CategoryStorage


class CategoriesController:
    def __init__(self, category_storage):
        self.category_storage = category_storage

    def create(category):
        category_storage.create(category)

    def update(category):
        category_storage.update(category)

    def delete(category_id):
        category_storage.delete_by_id(category_id)
