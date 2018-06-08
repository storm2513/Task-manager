import enum


class Status(enum.Enum):
    """
    Enum that stores values of notification's statuses
    CREATED - Notification was created
    PENDING - Notification should be shown
    SHOWN - Notification was shown
    """

    CREATED = 0
    PENDING = 1
    SHOWN = 2


class Notification:
    """Notification class that is used remind user about task"""

    def __init__(
            self,
            task_id,
            title,
            relative_start_time,
            status=Status.CREATED.value,
            id=None,
            user_id=None,):
        self.id = id
        self.user_id = user_id
        self.task_id = task_id
        self.title = title
        self.relative_start_time = relative_start_time
        self.status = status
