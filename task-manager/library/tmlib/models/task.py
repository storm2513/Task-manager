import enum


class Priority(enum.Enum):
    """Enum that stores values of task's priorities"""

    MIN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAX = 4


class Status(enum.Enum):
    """Enum that stores values of task's statuses"""

    TODO = 0
    IN_PROGRESS = 1
    DONE = 2
    ARCHIVED = 3
    TEMPLATE = 4


class Task:
    def __init__(
            self,
            title,
            note="",
            user_id=None,
            id=None,
            start_time=None,
            end_time=None,
            assigned_user_id=None,
            parent_task_id=None,
            is_event=False,
            category_id=None,
            priority=Priority.MEDIUM.value,
            status=Status.TODO.value,
            plan_id=None,
            created_at=None,
            updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.note = note
        self.start_time = start_time
        self.end_time = end_time
        self.assigned_user_id = assigned_user_id
        self.parent_task_id = parent_task_id
        self.is_event = is_event
        self.category_id = category_id
        self.priority = priority
        self.status = status
        self.plan_id = plan_id
        self.created_at = created_at
        self.updated_at = updated_at
