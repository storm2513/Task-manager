from storage.user_storage import UserStorage

class UsersController:
    def __init__(self, user_storage):
        self.user_storage = user_storage

    def create(user):
        user.level_id = LevelsController.create().id
        user_storage.create(user)

    def update(user):
        user_storage.update(user)

    def delete(user_id):
        user_storage.delete_by_id(user_id)
