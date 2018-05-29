class TaskPlansController:
    """
    Class for managing task plans
    """

    def __init__(self, plan_storage):
        """
        Storage field for access to database
        """

        self.plan_storage = plan_storage

    def create(self, plan):
        """
        Creates task plan
        """

        return self.plan_storage.create(plan)

    def update(self, plan):
        """
        Updates task plan
        """

        self.plan_storage.update(plan)

    def delete(self, plan_id):
        """
        Deletes task plan by ID
        """

        self.plan_storage.delete_by_id(plan_id)

    def get_by_id(self, plan_id):
        """
        Returns task plan by ID
        """

        return self.plan_storage.get_by_id(plan_id)

    def all(self, user_id):
        """
        Returns all user's task plans
        """

        return self.plan_storage.all_user_plans(user_id)

    def process_plans(self):
        """
        Creates tasks according to task plans. 
        """

        self.plan_storage.process_plans()
