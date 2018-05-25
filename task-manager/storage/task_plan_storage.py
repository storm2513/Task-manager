from storage.storage_models import Task, TaskPlan
from storage.task_storage import TaskStorage
from models.task_plan import TaskPlan as TaskPlanInstance
from enums.status import Status
import datetime
from peewee import *


class TaskPlanStorage:
    """
    Class for managing task plans in database
    """

    def create(self, plan):
        """
        Creates task plan
        """

        return self.to_plan_instance(
            TaskPlan.create(
                id=plan.id,
                interval=plan.interval,
                user_id=plan.user_id,
                task_id=plan.task_id,
                last_created_at=plan.last_created_at))

    def delete_by_id(self, plan_id):
        """
        Deletes task plan by ID
        """

        TaskPlan.delete().where(TaskPlan.id == plan_id).execute()

    def update(self, plan):
        """
        Updates task plan's interval and last_created_at fields
        """

        TaskPlan.update(
            interval=plan.interval,
            last_created_at=plan.last_created_at).where(
            TaskPlan.id == plan.id).execute()

    def to_plan_instance(self, plan):
        """
        Makes cast from TaskPlan class to TaskPlanInstance class
        """

        return TaskPlanInstance(
            id=plan.id,
            interval=plan.interval,
            user_id=plan.user_id,
            task_id=plan.task_id,
            last_created_at=plan.last_created_at)

    def get_by_id(self, plan_id):
        """
        Returns task plan by ID
        """

        try:
            return self.to_plan_instance(
                TaskPlan.get(TaskPlan.id == plan_id))
        except DoesNotExist:
            return None

    def all_user_plans(self, user_id):
        """
        Returns all user's task plans
        """

        return list(map(self.to_plan_instance, list(
            TaskPlan.select().where(TaskPlan.user_id == user_id))))

    def process_plans(self):
        """
        Creates tasks according to task plans. 
        """

        for plan in TaskPlan.select():
            if plan.last_created_at + datetime.timedelta(seconds=plan.interval) < datetime.datetime.now():
                try:
                    task_storage = TaskStorage()
                    task = task_storage.get_by_id(plan.task_id) # template task
                    task.id = None
                    task.status = Status.TODO.value # change status from TEMPLATE to TODO
                    task_storage.create(task)
                    """
                    last_created_at shouldn't offset the interval. 
                    E.g. user wants to plan task for every monday on 10:00. 
                    If this method called on tuesday in last_created_at should be monday 
                    in order to save the rule that it creates task every monday on 10:00.
                    """
                    last_created_at = plan.last_created_at + datetime.timedelta(seconds=plan.interval)
                    while last_created_at + datetime.timedelta(seconds=plan.interval) < datetime.datetime.now():
                        last_created_at += datetime.timedelta(seconds=plan.interval)
                    plan.last_created_at = last_created_at
                    plan.save()
                except DoesNotExist:
                    pass
