from storage.level_storage import LevelStorage

class LevelsController:
    TASK_COMPLETED_SCORE = 1

    def __init__(self, level_storage):
        self.level_storage = level_storage

    def create():
        return level_storage.create()

    def increase_experience(level_id)
        level = level_storage.get_by_id(level_id)
        level.experience += self.TASK_COMPLETED_SCORE
        level_storage.update(level)

    def delete(level_id):
        level_storage.delete_by_id(level_id)
