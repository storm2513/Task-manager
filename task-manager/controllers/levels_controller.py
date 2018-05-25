from storage.level_storage import LevelStorage


class LevelsController:
    """
    Class for managing levels
    """

    TASK_COMPLETED_SCORE = 1 # amount of experience for 1 completed task 

    def __init__(self, level_storage):
        """
        Storage field for access to database
        """

        self.level_storage = level_storage

    def create(self):
        """
        Creates level
        """

        return self.level_storage.create()

    def increase_experience(self, level):
        """
        Increases experience in level object
        """

        level.experience += self.TASK_COMPLETED_SCORE
        self.level_storage.update(level)

    def delete(self, level_id):
        """
        Deletes level by ID
        """

        self.level_storage.delete_by_id(level_id)

    def get_by_user_id(self, user_id):
        """
        Returns level by user ID
        """

        return self.level_storage.get_by_user_id(user_id)
