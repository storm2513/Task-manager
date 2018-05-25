from storage.category_storage import CategoryStorage


class CategoriesController:
    """
    Class for managing categories
    """

    def __init__(self, category_storage):
        """
        Storage field for access to database
        """

        self.category_storage = category_storage

    def create(self, category, user_id):
        """
        Creates category
        """

        category.user_id = user_id
        return self.category_storage.create(category)

    def update(self, category):
        """
        Updates category
        """

        return self.category_storage.update(category)

    def delete(self, category_id):
        """
        Deletes category by ID
        """

        self.category_storage.delete_by_id(category_id)

    def get_by_id(self, category_id):
        """
        Returns category by ID
        """

        return self.category_storage.get_by_id(category_id)

    def all(self, user_id):
        """
        Returns all categories for user with ID == user_id
        """

        return self.category_storage.all_user_categories(user_id)
