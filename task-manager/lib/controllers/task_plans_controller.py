from lib.controllers.base_controller import BaseController
from lib.storage.task_plan_storage import TaskPlanStorage


def create_task_plans_controller(user_id, database_name):
    return TaskPlansController(user_id, TaskPlanStorage(database_name))


class TaskPlansController(BaseController):
    """
    Class for managing task plans
    """

    def create(self, plan):
        return self.storage.create(plan)

    def update(self, plan):
        self.storage.update(plan)

    def delete(self, plan_id):
        self.storage.delete_by_id(plan_id)

    def get_by_id(self, plan_id):
        return self.storage.get_by_id(plan_id)

    def all(self):
        return self.storage.all_user_plans(self.user_id)

    def process_plans(self):
        """
        Creates tasks according to task plans. 
        """

        self.storage.process_plans()
