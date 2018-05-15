from storage.storage_models import Category
from models.category import Category as CategoryInstance

class CategoryStorage:
    @staticmethod
    def create(category):
        return Category.create(id=category.id, name=category.name, user_id=category.user_id)

    @staticmethod
    def delete_by_id(category_id):
        Category.delete().where(Category.id == category_id).execute()

    @staticmethod
    def update(category):
        Category.update(name=category.name).where(Category.id == category.id).execute()

    @staticmethod
    def to_category_instance(category):
        return CategoryInstance(
                id=category.id,
                experience=category.experience,
                user_id=category.user_id)

    @staticmethod
    def get_by_id(category_id):
        return CategoryStorage.to_category_instance(Category.get(Category.id == category_id))
