from storage.storage_models import Level
from models.level import Level as LevelInstance

class LevelStorage:
    @staticmethod
    def create():
        return Level.create()

    @staticmethod
    def delete_by_id(level_id):
        Level.delete().where(Level.id == level_id).execute()

    @staticmethod
    def update(level):
        Level.update(experience=level.experience).where(Level.id == level.id).execute()

    @staticmethod
    def to_level_instance(level):
        return LevelInstance(
                id=level.id,
                experience=level.experience)

    @staticmethod
    def get_by_id(level_id):
        return LevelStorage.to_level_instance(Level.get(Level.id == level_id))
