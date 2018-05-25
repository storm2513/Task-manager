from storage.storage_models import Level, User
from models.level import Level as LevelInstance
from peewee import *


class LevelStorage:
    """
    Class for managing levels in database
    """

    def create(self):
        """
        Creates user's level
        """

        return self.to_level_instance(Level.create())

    def delete_by_id(self, level_id):
        """
        Deletes level by it's ID
        """

        Level.delete().where(Level.id == level_id).execute()

    def update(self, level):
        """
        Updates level experience
        """

        Level.update(
            experience=level.experience).where(
            Level.id == level.id).execute()

    def to_level_instance(self, level):
        """
        Makes cast from Level class to LevelInstance class
        """

        return LevelInstance(
            id=level.id,
            experience=level.experience)

    def get_by_id(self, level_id):
        """
        Returns level by ID
        """

        try:
            return self.to_level_instance(Level.get(Level.id == level_id))
        except DoesNotExist:
            return None

    def get_by_user_id(self, user_id):
        """
        Returns user's level by user ID
        """

        try:
            level_id = User.select(
                User.level_id).where(
                User.id == user_id).first().level_id
            return self.get_by_id(level_id)
        except DoesNotExist:
            return None
