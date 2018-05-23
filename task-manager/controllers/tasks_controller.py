from storage.task_storage import TaskStorage
from enums.status import Status
from controllers.levels_controller import LevelsController
from storage.level_storage import LevelStorage


class TasksController:
    def __init__(self, task_storage):
        self.task_storage = task_storage

    def create(self, task):
        return self.task_storage.create(task)

    def update(self, task):
        self.task_storage.update(task)

    def delete(self, task_id):
        self.task_storage.delete_by_id(task_id)

    def set_as_to_do(self, task_id):
        task = self.get_by_id(task_id)
        task.status = Status.TODO.value
        self.update(task)

    def set_as_in_progress(self, task_id):
        task = self.get_by_id(task_id)
        task.status = Status.IN_PROGRESS.value
        self.update(task)

    def set_as_done(self, task_id):
        task = self.get_by_id(task_id)
        task.status = Status.DONE.value
        self.update(task)
        level = LevelsController(LevelStorage()).get_by_user_id(task.user_id)
        LevelsController(LevelStorage()).increase_experience(level)

    def set_as_archived(self, task_id):
        task = self.get_by_id(task_id)
        task.status = Status.ARCHIVED.value
        self.update(task)

    def user_tasks(self, user_id):
        return self.task_storage.user_tasks(user_id)

    def with_status(self, user_id, status):
        return self.task_storage.with_status(user_id, status)

    def get_by_id(self, task_id):
        return self.task_storage.get_by_id(task_id)

    def create_inner_task(self, parent_task_id, task):
        task.parent_task_id = parent_task_id
        return self.create(task)

    def inner(self, task_id):
        return self.task_storage.inner(task_id)

    def assign_task_on_user(self, task_id, user_id):
        task = self.get_by_id(task_id)
        task.assigned_user_id = user_id
        self.update(task)

    def assigned(self, user_id):
        return self.task_storage.assigned(user_id)

    def can_read(self, user_id):
        return self.task_storage.can_read(user_id)

    def can_write(self, user_id):
        return self.task_storage.can_write(user_id)

    def add_user_for_read(self, user_id, task_id):
        self.task_storage.add_user_for_read(user_id=user_id, task_id=task_id)

    def add_user_for_write(self, user_id, task_id):
        self.task_storage.add_user_for_write(user_id=user_id, task_id=task_id)

    def remove_user_for_read(self, user_id, task_id):
        self.task_storage.remove_user_for_read(
            user_id=user_id, task_id=task_id)

    def remove_user_for_write(self, user_id, task_id):
        self.task_storage.remove_user_for_write(
            user_id=user_id, task_id=task_id)

    def user_can_read(self, user_id, task_id):
        return self.task_storage.user_can_read(user_id, task_id)

    def user_can_write(self, user_id, task_id):
        return self.task_storage.user_can_write(user_id, task_id)
