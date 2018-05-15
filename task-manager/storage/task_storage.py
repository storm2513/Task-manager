from storage.storage_models import Task, UsersReadTasks, UsersWriteTasks
from models.task import Task as TaskInstance


class TaskStorage:
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
                category=task.category,
                priority=task.priority,
                status=task.status))

    def delete(self, task):
        Task.delete().where(Task.id == task.id).execute()

    def delete_by_id(self, task_id):
        Task.delete().where(Task.id == task_id).execute()

    def update(self, task):
        Task.update(
            title=task.title,
            note=task.note,
            start_time=task.start_time,
            end_time=task.end_time,
            assigned_user_id=task.assigned_user_id,
            is_event=task.is_event,
            category=task.category,
            priority=task.priority,
            status=task.status).where(Task.id == task.id).execute()

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
            status=task.status)

    def get_by_id(self, task_id):
        return self.to_task_instance(Task.get(Task.id == task_id))

    def user_tasks(self, user):
        return list(map(self.to_task_instance, list(
            Task.select().where(Task.user_id == user.id))))

    def inner(self, task):
        return list(map(self.to_task_instance, list(
            Task.select().where(Task.parent_task_id == task.id))))

    def add_user_for_read(user_id, task_id):
        if UsersReadTasks.select().where(UsersReadTasks.task_id ==
                                         task_id and UsersReadTasks.user_id == user_id).count() == 0:
            UsersReadTasks.create(user_id=user_id, task_id=task_id)

    def add_user_for_write(user_id, task_id):
        if UsersWriteTasks.select().where(UsersWriteTasks.task_id ==
                                          task_id and UsersWriteTasks.user_id == user_id).count() == 0:
            UsersWriteTasks.create(user_id=user_id, task_id=task_id)

    def remove_user_for_read(user_id, task_id):
        UsersReadTasks.delete().where(UsersReadTasks.user_id ==
                                      user_id and UsersReadTasks.task_id == task_id).execute()

    def remove_user_for_write(user_id, task_id):
        UsersWriteTasks.delete().where(UsersWriteTasks.user_id ==
                                       user_id and UsersWriteTasks.task_id == task_id).execute()
