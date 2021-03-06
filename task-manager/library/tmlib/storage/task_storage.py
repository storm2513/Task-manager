import datetime
from collections import deque
from peewee import DoesNotExist
from tmlib.storage.storage_models import (
    Task, UsersReadTasks, UsersWriteTasks, TaskPlan, DatabaseConnector)
from tmlib.models.task import Task as TaskInstance


class TaskStorage(DatabaseConnector):
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
                status=task.status,
                plan_id=task.plan_id))

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
            updated_at=task.updated_at,
            plan_id=task.plan_id)

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
        """Returns tasks that user can read"""

        return list(map(self.to_task_instance, list(Task.select().join(UsersReadTasks).where(
            UsersReadTasks.task_id == Task.id, UsersReadTasks.user_id == user_id))))

    def can_write(self, user_id):
        """Returns tasks that user can read and change"""

        return list(map(self.to_task_instance, list(Task.select().join(UsersWriteTasks).where(
            UsersWriteTasks.task_id == Task.id, UsersWriteTasks.user_id == user_id))))

    def inner(self, task_id, recursive=False):
        """Returns inner tasks for task with ID == task_id"""
        if recursive:
            queue = deque()
            queue.append(self.get_by_id(task_id))
            inner_tasks = []
            return self.recursive_inner(queue, inner_tasks)

        return list(map(self.to_task_instance, list(
            Task.select().where(Task.parent_task_id == task_id))))

    def recursive_inner(self, queue, inner_tasks):
        """
        Returns all inner tasks using BFS
        """

        if not queue:
            return inner_tasks

        task = queue.popleft()
        for inner_task in self.inner(task.id):
            inner_tasks.append(inner_task)
            queue.append(inner_task)

        return self.recursive_inner(queue, inner_tasks)

    def add_user_for_read(self, user_id, task_id):
        """Allows user with ID == user_id to read task with ID == task_id"""

        if UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id,
                UsersReadTasks.user_id == user_id).count() == 0:
            UsersReadTasks.create(user_id=user_id, task_id=task_id)

    def add_user_for_write(self, user_id, task_id):
        """Allows user with ID == user_id to read and change task with ID == task_id"""

        if UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id,
                UsersWriteTasks.user_id == user_id).count() == 0:
            UsersWriteTasks.create(user_id=user_id, task_id=task_id)

    def remove_user_for_read(self, user_id, task_id):
        """Removes permission to read task with ID == task_id from user with ID == user_id"""

        UsersReadTasks.delete().where(
            UsersReadTasks.user_id == user_id,
            UsersReadTasks.task_id == task_id).execute()

    def remove_all_users_for_read(self, task_id):
        UsersReadTasks.delete().where(
            UsersReadTasks.task_id == task_id).execute()

    def remove_user_for_write(self, user_id, task_id):
        """Removes permission to read and change task with ID == task_id from user with ID == user_id"""

        UsersWriteTasks.delete().where(
            UsersWriteTasks.user_id == user_id,
            UsersWriteTasks.task_id == task_id).execute()

    def remove_all_users_for_write(self, task_id):
        UsersWriteTasks.delete().where(
            UsersWriteTasks.task_id == task_id).execute()

    def get_users_can_read_task(self, task_id):
        users_list = list(UsersReadTasks.select(
            UsersReadTasks.user_id).where(UsersReadTasks.task_id == task_id))
        return [element.user_id for element in users_list]

    def get_users_can_write_task(self, task_id):
        users_list = list(UsersWriteTasks.select(
            UsersWriteTasks.user_id).where(UsersWriteTasks.task_id == task_id))
        return [element.user_id for element in users_list]

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

    def filter(self, *args):
        """
        Before usage you should import Task from tmlib.storage.storage_models module.
        Then you can pass filter query.
        If you want to filter multiple fields use bitwise operators (& and |) rather than logical operators (and and or).

        Example:
        filter(Task.title.contains('title') & Task.created_at > datetime.datetime.now())
        """

        return list(map(self.to_task_instance,
                        list(Task.select().where(args))))

    def created_by_task_plan(self, user_id, plan_id):
        return list(map(self.to_task_instance, list(Task.select().where(
            Task.user_id == user_id, Task.plan_id == plan_id))))
