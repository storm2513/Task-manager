from storage.storage_models import User
from models.user import User as UserInstance

class UserStorage:
    @staticmethod
    def create(user):
        User.create(id=user.id,
                    email=user.email,
                    name=user.name,
                    password=user.password,
                    level_id=user.level_id)

    @staticmethod
    def delete(user):
        User.delete().where(User.id == user.id).execute()

    @staticmethod
    def delete_by_id(user_id):
        User.delete().where(User.id == user_id).execute()

    @staticmethod
    def update(user):
        User.update(
            email=user.email,
            name=user.name,
            password=user.password).where(User.id == user.id).execute()

    @staticmethod
    def to_user_instance(user):
        return UserInstance(
                id=user.id,
                email=user.email,
                name=user.name,
                password=user.password,
                level_id=user.level_id)

    @staticmethod
    def get_by_id(user_id):
        return UserStorage.to_user_instance(User.get(User.id == user_id))
