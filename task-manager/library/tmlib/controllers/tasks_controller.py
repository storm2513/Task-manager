from tmlib.storage.task_storage import TaskStorage
from tmlib.models.task import Status
from tmlib.controllers.base_controller import BaseController


def create_tasks_controller(user_id, database_name):
    return TasksController(user_id, TaskStorage(database_name))


class TasksController(BaseController):
    def create(self, task):
        task.user_id = self.user_id
        return self.storage.create(task)

    def update(self, task):
        self.storage.update(task)

    def delete(self, task_id):
        self.storage.delete_by_id(task_id)

    def set_status(self, task_id, status):
        task = self.get_by_id(task_id)
        task.status = status
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

    def inner(self, task_id, recursive=False):
        """Returns inner tasks for task with ID == task_id"""

        return self.storage.inner(task_id, recursive)

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

    def remove_all_users_for_read(self, task_id):
        self.storage.remove_all_users_for_read(task_id=task_id)

    def remove_user_for_write(self, user_id, task_id):
        """Removes permission to read and change task with ID == task_id from user with ID == user_id"""

        self.storage.remove_user_for_write(
            user_id=user_id, task_id=task_id)

    def remove_all_users_for_write(self, task_id):
        self.storage.remove_all_users_for_write(task_id=task_id)

    def get_users_can_read_task(self, task_id):
        return self.storage.get_users_can_read_task(task_id)

    def get_users_can_write_task(self, task_id):
        return self.storage.get_users_can_write_task(task_id)

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

    def filter(self, *args):
        """
        Before usage you should import Task from tmlib.storage.storage_models module.
        Then you can pass filter query.
        If you want to filter multiple fields use bitwise operators (& and |) rather than logical operators (and and or).

        Example:
        filter(Task.title.contains('title') & Task.created_at > datetime.datetime.now())
        """

        return self.storage.filter(args)

    def created_by_task_plan(self, plan_id):
        return self.storage.created_by_task_plan(self.user_id, plan_id)
