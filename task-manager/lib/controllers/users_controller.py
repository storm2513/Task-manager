from lib.storage.user_storage import UserStorage
from lib.controllers.levels_controller import LevelsController
from lib.storage.level_storage import LevelStorage


class UsersController:
    """
    Class for managing users
    """

    def __init__(self, user_storage):
        """
        Storage field for access to database
        """

        self.user_storage = user_storage

    def create(self, user):
        """
        Creates user with level
        """

        user.level_id = LevelsController(LevelStorage()).create().id
        return self.user_storage.create(user)

    def update(self, user):
        """
        Updates user
        """

        self.user_storage.update(user)

    def delete(self, user_id):
        """
        Deletes user by ID
        """

        level_id = self.get_by_id(user_id).level_id
        self.user_storage.delete_by_id(user_id)
        LevelsController(LevelStorage()).delete(level_id)

    def get_by_id(self, user_id):
        """
        Returns user by it's ID
        """

        return self.user_storage.get_by_id(user_id)

    def get_by_email(self, email):
        """
        Returns user by it's email
        """

        return self.user_storage.get_by_email(email)

    def all(self):
        """
        Returns list of all users without passwords
        """

        return self.user_storage.all_users()
