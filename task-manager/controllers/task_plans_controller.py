class TaskPlansController:
    def __init__(self, plan_storage):
        self.plan_storage = plan_storage

    def create(self, plan):
        return self.plan_storage.create(plan)

    def update(self, plan):
        self.plan_storage.update(plan)

    def delete(self, plan_id):
        self.plan_storage.delete_by_id(plan_id)

    def get_by_id(self, plan_id):
        return self.plan_storage.get_by_id(plan_id)

    def all(self, user_id):
        return self.plan_storage.all_user_plans(user_id)

    def process_plans(self):
        self.plan_storage.process_plans()
