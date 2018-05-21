from storage.user_storage import UserStorage
from controllers.levels_controller import LevelsController
from storage.level_storage import LevelStorage


class UsersController:
    def __init__(self, user_storage):
        self.user_storage = user_storage

    def create(self, user):
        user.level_id = LevelsController(LevelStorage()).create().id
        return self.user_storage.create(user)

    def update(self, user):
        self.user_storage.update(user)

    def delete(self, user_id):
        level_id = self.get_by_id(user_id).level_id
        self.user_storage.delete_by_id(user_id)
        LevelsController(LevelStorage()).delete(level_id)

    def get_by_id(self, user_id):
        return self.user_storage.get_by_id(user_id)

    def get_by_email(self, email):
        return self.user_storage.get_by_email(email)

    def all(self):
        return self.user_storage.all_users()
