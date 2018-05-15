from storage.task_storage import TaskStorage
from enums.status import Status
from controllers.levels_controller import LevelsController


class TasksController:
    def __init__(self, task_storage):
        self.task_storage = task_storage

    def create(self, task):
        self.task_storage.create(task)

    def update(self, task):
        self.task_storage.update(task)

    def delete(self, task_id):
        self.task_storage.delete_by_id(task_id)

    def set_as_to_do(self, task):
        task.status = Status.TODO
        self.update(task)

    def set_as_in_progress(self, task):
        task.status = Status.IN_PROGRESS
        self.update(task)

    def set_as_complete(self, task):
        task.status = Status.DONE
        self.update(task)
        level = LevelsController.get_by_user_id(task.user_id)
        LevelsController.increase_experience(level)

    def set_as_archive(self, task):
        task.status = Status.ARCHIVED
        self.update(task)

    def user_tasks(self, user):
        return self.task_storage.user_tasks(user)

    def get_by_id(self, task_id):
        return self.task_storage.get_by_id(task_id)

    def create_inner_task(self, parent_task_id, task):
        task.parent_task_id = parent_task_id
        self.update(task)

    def assign_user_on_task(self, user_id, task):
        task.assigned_user_id = user_id
        self.update(task)

    def add_user_for_read(user_id, task_id):
        self.task_storage.add_user_for_read(user_id=user_id, task_id=task_id)

    def add_user_for_write(user_id, task_id):
        self.task_storage.add_user_for_read(user_id=user_id, task_id=task_id)

    def remove_user_for_read(user_id, task_id):
        self.task_storage.remove_user_for_read(
            user_id=user_id, task_id=task_id)

    def add_user_for_write(user_id, task_id):
        self.task_storage.remove_user_for_read(
            user_id=user_id, task_id=task_id)
