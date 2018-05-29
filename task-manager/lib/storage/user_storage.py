from lib.storage.storage_models import User
from lib.models.user import User as UserInstance
from peewee import *


class UserStorage:
    """
    Class for managing users in database
    """

    def create(self, user):
        """
        Creates user
        """

        return self.to_user_instance(User.create(id=user.id,
                                                 email=user.email,
                                                 name=user.name,
                                                 password=user.password,
                                                 level_id=user.level_id))

    def delete_by_id(self, user_id):
        """
        Deletes user by it's ID
        """

        User.delete().where(User.id == user_id).execute()

    def update(self, user):
        """
        Updates user's email, name and password
        """

        User.update(
            email=user.email,
            name=user.name,
            password=user.password).where(User.id == user.id).execute()

    def to_user_instance(self, user):
        """
        Makes cast from User class to UserInstance class
        """

        return UserInstance(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            level_id=user.level_id)

    def get_by_id(self, user_id):
        """
        Returns user by ID
        """

        try:
            return self.to_user_instance(User.get(User.id == user_id))
        except DoesNotExist:
            return None

    def get_by_email(self, email):
        """
        Returns user by email
        """

        try:
            return self.to_user_instance(User.get(User.email == email))
        except DoesNotExist:
            return None

    def all_users(self):
        """
        Returns list of all users without passwords
        """

        return list(map(self.to_user_instance, list(User.select(User.id, User.email, User.name))))
