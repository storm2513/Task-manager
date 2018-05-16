from storage.storage_models import Category
from models.category import Category as CategoryInstance
from peewee import *


class CategoryStorage:
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
