from tmlib.storage.task_storage import TaskStorage
from tmlib.models.task import Status
from tmlib.controllers.base_controller import BaseController


def create_tasks_controller(user_id, database_name):
    return TasksController(user_id, TaskStorage(database_name))


class TasksController(BaseController):
    """Class for managing tasks"""

    def create(self, task):
        return self.storage.create(task)

    def update(self, task):
        self.storage.update(task)

    def delete(self, task_id):
        self.storage.delete_by_id(task_id)

    def set_as_to_do(self, task_id):
        """Sets task's status as TODO by ID"""

        task = self.get_by_id(task_id)
        task.status = Status.TODO.value
        self.update(task)

    def set_as_in_progress(self, task_id):
        """Sets task's status as IN_PROGRESS by ID"""

        task = self.get_by_id(task_id)
        task.status = Status.IN_PROGRESS.value
        self.update(task)

    def set_as_done(self, task_id):
        """Sets task's status as DONE by ID"""

        task = self.get_by_id(task_id)
        task.status = Status.DONE.value
        self.update(task)

    def set_as_archived(self, task_id):
        """Sets task's status as ARCHIVED by ID"""

        task = self.get_by_id(task_id)
        task.status = Status.ARCHIVED.value
        self.update(task)

    def user_tasks(self):
        return self.storage.user_tasks(self.user_id)

    def with_status(self, status):
        """Returns user's tasks with provided status"""

        return self.storage.with_status(self.user_id, status)

    def get_by_id(self, task_id):
        return self.storage.get_by_id(task_id)

    def create_inner_task(self, parent_task_id, task):
        task.parent_task_id = parent_task_id
        return self.create(task)

    def inner(self, task_id):
        """Returns inner tasks for task with ID == task_id"""

        return self.storage.inner(task_id)

    def assign_task_on_user(self, task_id, user_id):
        task = self.get_by_id(task_id)
        task.assigned_user_id = user_id
        self.update(task)

    def assigned(self):
        """Returns assigned tasks for user"""

        return self.storage.assigned(self.user_id)

    def can_read(self):
        """Returns tasks that user can read"""

        return self.storage.can_read(self.user_id)

    def can_write(self):
        """Returns tasks that user can read and change"""

        return self.storage.can_write(self.user_id)

    def add_user_for_read(self, user_id, task_id):
        """Allows user with ID == user_id to read task with ID == task_id"""

        self.storage.add_user_for_read(user_id=user_id, task_id=task_id)

    def add_user_for_write(self, user_id, task_id):
        """Allows user with ID == user_id to read and change task with ID == task_id"""

        self.storage.add_user_for_write(user_id=user_id, task_id=task_id)

    def remove_user_for_read(self, user_id, task_id):
        """Removes permission to read task with ID == task_id from user with ID == user_id"""

        self.storage.remove_user_for_read(
            user_id=user_id, task_id=task_id)

    def remove_user_for_write(self, user_id, task_id):
        """Removes permission to read and change task with ID == task_id from user with ID == user_id"""

        self.storage.remove_user_for_write(
            user_id=user_id, task_id=task_id)

    def user_can_read(self, task_id):
        """
        Returns True if user with ID == user_id can read task with ID == task_id.
        Otherwise returns False
        """

        return self.storage.user_can_read(self.user_id, task_id)

    def user_can_write(self, task_id):
        """
        Returns True if user with ID == user_id can read and change task with ID == task_id.
        Otherwise returns False
        """

        return self.storage.user_can_write(self.user_id, task_id)
