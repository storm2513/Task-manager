from lib.storage.storage_models import Category
from lib.models.category import Category as CategoryInstance
from peewee import *


class CategoryStorage:
    """
    Class for managing categories in database
    """

    def create(self, category):
        """
        Creates category from CategoryInstance class
        """

        return self.to_category_instance(
            Category.create(
                id=category.id,
                name=category.name,
                user_id=category.user_id))

    def delete_by_id(self, category_id):
        """
        Deletes category by id
        """

        Category.delete().where(Category.id == category_id).execute()

    def update(self, category):
        """
        Updates category name
        """

        Category.update(
            name=category.name).where(
            Category.id == category.id).execute()

    def to_category_instance(self, category):
        """
        Makes cast from Category class to CategoryInstance class
        """

        return CategoryInstance(
            id=category.id,
            name=category.name,
            user_id=category.user_id)

    def get_by_id(self, category_id):
        """
        Returns category by it's ID
        """

        try:
            return self.to_category_instance(
                Category.get(Category.id == category_id))
        except DoesNotExist:
            return None

    def all_user_categories(self, user_id):
        """
        Returns all categories for user with id == user_id
        """

        return list(map(self.to_category_instance, list(Category.select().where(Category.user_id == user_id))))
