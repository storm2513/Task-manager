from storage.level_storage import LevelStorage


class LevelsController:
    TASK_COMPLETED_SCORE = 1

    def __init__(self, level_storage):
        self.level_storage = level_storage

    def create(self):
        return self.level_storage.create()

    def increase_experience(self, level_id):
        level = self.level_storage.get_by_id(level_id)
        level.experience += self.TASK_COMPLETED_SCORE
        self.level_storage.update(level)

    def delete(self, level_id):
        self.level_storage.delete_by_id(level_id)
