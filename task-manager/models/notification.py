from enums.notification_status import NotificationStatus


class Notification:
    def __init__(
            self,
            task_id,
            title,
            relative_start_time,
            status=NotificationStatus.CREATED.value,
            id=None,
            user_id=None,):
        self.id = id
        self.user_id = user_id
        self.task_id = task_id
        self.title = title
        self.relative_start_time = relative_start_time
        self.status = status
