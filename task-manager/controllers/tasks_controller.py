from storage.task_storage import TaskStorage


class TasksController:
    def __init__(self, task_storage):
        self.task_storage = task_storage

    def create(self, task):
        self.task_storage.create(task)

    def update(self, task):
        self.task_storage.update(task)

    def delete(self, task_id):
        self.task_storage.delete_by_id(task_id)

    def user_tasks(self, user):
        return self.task_storage.user_tasks(user)

    def get_by_id(self, task_id):
        return self.task_storage.get_by_id(task_id)
