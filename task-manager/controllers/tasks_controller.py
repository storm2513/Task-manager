from storage.task_storage import TaskStorage

class TasksController:
    def __init__(self, task_storage):
        self.task_storage = task_storage

    def create(task):
        task_storage.create(task)

    def update(task):
        task_storage.update(task)

    def delete(task_id):
        task_storage.delete_by_id(task_id)
