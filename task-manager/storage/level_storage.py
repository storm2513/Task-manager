from storage.storage_models import Level, User
from models.level import Level as LevelInstance


class LevelStorage:
    def create(self):
        return Level.create()

    def delete_by_id(self, level_id):
        Level.delete().where(Level.id == level_id).execute()

    def update(self, level):
        Level.update(
            experience=level.experience).where(
            Level.id == level.id).execute()

    def to_level_instance(self, level):
        return LevelInstance(
            id=level.id,
            experience=level.experience)

    def get_by_id(self, level_id):
        return self.to_level_instance(Level.get(Level.id == level_id))

    def get_by_user_id(self, user_id):
        level_id = User.select(
            User.level_id).where(
            User.id == user_id).first().level_id
        return self.get_by_id(level_id)
