from storage.storage_models import Task
from models.task import Task as TaskInstance


class TaskStorage:
    @staticmethod
    def create(task):
        Task.create(id=task.id,
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
                    status=task.status)

    @staticmethod
    def delete(task):
        Task.delete().where(Task.id == task.id).execute()

    @staticmethod
    def delete_by_id(task_id):
        Task.delete().where(Task.id == task_id).execute()

    @staticmethod
    def update(task):
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

    @staticmethod
    def to_task_instance(task):
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

    @staticmethod
    def get_by_id(task_id):
        return TaskStorage.to_task_instance(Task.get(Task.id == task_id))

