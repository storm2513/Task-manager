from storage.storage_models import User
from models.user import User as UserInstance
from peewee import *


class UserStorage:
    def create(self, user):
        return self.to_user_instance(User.create(id=user.id,
                                                 email=user.email,
                                                 name=user.name,
                                                 password=user.password,
                                                 level_id=user.level_id))

    def delete_by_id(self, user_id):
        User.delete().where(User.id == user_id).execute()

    def update(self, user):
        User.update(
            email=user.email,
            name=user.name,
            password=user.password).where(User.id == user.id).execute()

    def to_user_instance(self, user):
        return UserInstance(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            level_id=user.level_id)

    def get_by_id(self, user_id):
        try:
            return self.to_user_instance(User.get(User.id == user_id))
        except DoesNotExist:
            return None

    def get_by_email(self, email):
        try:
            return self.to_user_instance(User.get(User.email == email))
        except DoesNotExist:
            return None
