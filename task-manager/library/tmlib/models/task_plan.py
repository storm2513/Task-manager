class TaskPlan:
    """Class that creates task from template according to interval"""

    def __init__(
            self,
            interval,
            user_id,
            task_id,
            last_created_at,
            id=None):
        self.id = id
        self.user_id = user_id
        self.task_id = task_id
        self.interval = interval
        self.last_created_at = last_created_at
