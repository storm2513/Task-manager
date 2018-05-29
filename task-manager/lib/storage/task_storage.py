from lib.storage.storage_models import Task, UsersReadTasks, UsersWriteTasks, TaskPlan, Adapter
from lib.models.task import Task as TaskInstance
from peewee import *
import datetime


class TaskStorage(Adapter):
    """
    Class for managing tasks in database
    """

    def create(self, task):
        return self.to_task_instance(
            Task.create(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                note=task.note,
                start_time=task.start_time,
                end_time=task.end_time,
                assigned_user_id=task.assigned_user_id,
                parent_task_id=task.parent_task_id,
                is_event=task.is_event,
                category_id=task.category_id,
                priority=task.priority,
                status=task.status))

    def delete_by_id(self, task_id):
        Task.delete().where(Task.id == task_id).execute()
        TaskPlan.delete().where(TaskPlan.task_id == task_id).execute()

    def update(self, task):
        Task.update(
            title=task.title,
            note=task.note,
            start_time=task.start_time,
            end_time=task.end_time,
            assigned_user_id=task.assigned_user_id,
            is_event=task.is_event,
            category_id=task.category_id,
            priority=task.priority,
            status=task.status,
            parent_task_id=task.parent_task_id,
            updated_at=datetime.datetime.now()).where(
            Task.id == task.id).execute()

    def to_task_instance(self, task):
        return TaskInstance(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            note=task.note,
            start_time=task.start_time,
            end_time=task.end_time,
            assigned_user_id=task.assigned_user_id,
            parent_task_id=task.parent_task_id,
            is_event=task.is_event,
            category_id=task.category_id,
            priority=task.priority,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at)

    def get_by_id(self, task_id):
        try:
            return self.to_task_instance(Task.get(Task.id == task_id))
        except DoesNotExist:
            return None

    def user_tasks(self, user_id):
        return list(map(self.to_task_instance, list(
            Task.select().where(Task.user_id == user_id))))

    def assigned(self, user_id):
        return list(map(self.to_task_instance, list(
            Task.select().where(Task.assigned_user_id == user_id))))

    def with_status(self, user_id, status):
        return list(map(self.to_task_instance, list(
            Task.select().where(Task.user_id == user_id, Task.status == status))))

    def can_read(self, user_id):
        """
        Returns tasks that user can read
        """

        return list(map(self.to_task_instance, list(Task.select().join(UsersReadTasks).where(
            UsersReadTasks.task_id == Task.id, UsersReadTasks.user_id == user_id))))

    def can_write(self, user_id):
        """
        Returns tasks that user can read and change
        """

        return list(map(self.to_task_instance, list(Task.select().join(UsersWriteTasks).where(
            UsersWriteTasks.task_id == Task.id, UsersWriteTasks.user_id == user_id))))

    def inner(self, task_id):
        """
        Returns inner tasks for task with ID == task_id
        """

        return list(map(self.to_task_instance, list(
            Task.select().where(Task.parent_task_id == task_id))))

    def add_user_for_read(self, user_id, task_id):
        """
        Allows user with ID == user_id to read task with ID == task_id
        """

        if UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id,
                UsersReadTasks.user_id == user_id).count() == 0:
            UsersReadTasks.create(user_id=user_id, task_id=task_id)

    def add_user_for_write(self, user_id, task_id):
        """
        Allows user with ID == user_id to read and change task with ID == task_id
        """

        if UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id,
                UsersWriteTasks.user_id == user_id).count() == 0:
            UsersWriteTasks.create(user_id=user_id, task_id=task_id)

    def remove_user_for_read(self, user_id, task_id):
        """
        Removes permission to read task with ID == task_id from user with ID == user_id
        """

        UsersReadTasks.delete().where(
            UsersReadTasks.user_id == user_id,
            UsersReadTasks.task_id == task_id).execute()

    def remove_user_for_write(self, user_id, task_id):
        """
        Removes permission to read and change task with ID == task_id from user with ID == user_id
        """

        UsersWriteTasks.delete().where(
            UsersWriteTasks.user_id == user_id,
            UsersWriteTasks.task_id == task_id).execute()

    def user_can_read(self, user_id, task_id):
        """
        Returns True if user with ID == user_id can read task with ID == task_id.
        Otherwise returns False
        """

        return UsersReadTasks.select().where(
            UsersReadTasks.task_id == task_id,
            UsersReadTasks.user_id == user_id).count() == 1

    def user_can_write(self, user_id, task_id):
        """
        Returns True if user with ID == user_id can read and change task with ID == task_id.
        Otherwise returns False
        """

        return UsersWriteTasks.select().where(
            UsersWriteTasks.task_id == task_id,
            UsersWriteTasks.user_id == user_id).count() == 1
