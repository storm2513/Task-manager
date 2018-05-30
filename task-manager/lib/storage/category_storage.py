from lib.storage.storage_models import Category, Adapter
from lib.models.category import Category as CategoryInstance
from peewee import DoesNotExist


class CategoryStorage(Adapter):
    """
    Class for managing categories in database
    """

    def create(self, category):
        return self.to_category_instance(
            Category.create(
                id=category.id,
                name=category.name,
                user_id=category.user_id))

    def delete_by_id(self, category_id):
        Category.delete().where(Category.id == category_id).execute()

    def update(self, category):
        Category.update(
            name=category.name).where(
            Category.id == category.id).execute()

    def to_category_instance(self, category):
        return CategoryInstance(
            id=category.id,
            name=category.name,
            user_id=category.user_id)

    def get_by_id(self, category_id):
        try:
            return self.to_category_instance(
                Category.get(Category.id == category_id))
        except DoesNotExist:
            return None

    def all_user_categories(self, user_id):
        return list(map(self.to_category_instance, list(
            Category.select().where(Category.user_id == user_id))))
