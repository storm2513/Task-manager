from storage.storage_models import Task, TaskPlan
from storage.task_storage import TaskStorage
from models.task_plan import TaskPlan as TaskPlanInstance
from enums.status import Status
import datetime
from peewee import *


class TaskPlanStorage:
    def create(self, plan):
        return self.to_plan_instance(
            TaskPlan.create(
                id=plan.id,
                interval=plan.interval,
                user_id=plan.user_id,
                task_id=plan.task_id,
                last_created_at=plan.last_created_at))

    def delete_by_id(self, plan_id):
        TaskPlan.delete().where(TaskPlan.id == plan_id).execute()

    def update(self, plan):
        TaskPlan.update(
            interval=plan.interval,
            last_created_at=plan.last_created_at).where(
            TaskPlan.id == plan.id).execute()

    def to_plan_instance(self, plan):
        return TaskPlanInstance(
            id=plan.id,
            interval=plan.interval,
            user_id=plan.user_id,
            task_id=plan.task_id,
            last_created_at=plan.last_created_at)

    def get_by_id(self, plan_id):
        try:
            return self.to_plan_instance(
                TaskPlan.get(TaskPlan.id == plan_id))
        except DoesNotExist:
            return None

    def all_user_plans(self, user_id):
        return list(map(self.to_plan_instance, list(
            TaskPlan.select().where(TaskPlan.user_id == user_id))))

    def process_plans(self):
        for plan in TaskPlan.select():
            if plan.last_created_at + datetime.timedelta(seconds=plan.interval) < datetime.datetime.now():
                try:
                    task_storage = TaskStorage()
                    task = task_storage.get_by_id(plan.task_id)
                    task.id = None
                    task.status = Status.TODO.value
                    task_storage.create(task)
                    last_created_at = plan.last_created_at + datetime.timedelta(seconds=plan.interval)
                    while last_created_at + datetime.timedelta(seconds=plan.interval) < datetime.datetime.now():
                        last_created_at += datetime.timedelta(seconds=plan.interval)
                    plan.last_created_at = last_created_at
                    plan.save()
                except DoesNotExist:
                    pass
