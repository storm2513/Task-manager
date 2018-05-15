from enums.priority import Priority
from enums.status import Status


class Task:
    def __init__(
            self,
            user_id,
            title,
            note="",
            id=None,
            start_time=None,
            end_time=None,
            assigned_user_id=None,
            parent_task_id=None,
            is_event=False,
            category_id=None,
            priority=Priority.MEDIUM,
            status=Status.TODO):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.note = note
        self.start_time = start_time
        self.end_time = end_time
        self.assigned_user_id = assigned_user_id
        self.parent_task_id = parent_task_id
        self.is_event = is_event
        self.category = category_id
        self.priority = priority
        self.status = Status.TODO
