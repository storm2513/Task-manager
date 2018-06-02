from tmlib.storage.notification_storage import NotificationStorage
from tmlib.models.notification import Status as NotificationStatus
from tmlib.controllers.base_controller import BaseController


def create_notifications_controller(user_id, database_name):
    return NotificationsController(user_id, NotificationStorage(database_name))


class NotificationsController(BaseController):
    """Class for managing notifications"""

    def create(self, notification):
        notification.user_id = self.user_id
        return self.storage.create(notification)

    def update(self, notification):
        self.storage.update(notification)

    def delete(self, notification_id):
        self.storage.delete_by_id(notification_id)

    def get_by_id(self, notification_id):
        return self.storage.get_by_id(notification_id)

    def all(self):
        return self.storage.all_user_notifications(self.user_id)

    def set_as_shown(self, notification_id):
        """Sets notification's status with ID == notification_id as SHOWN"""

        notification = self.get_by_id(notification_id)
        notification.status = NotificationStatus.SHOWN.value
        self.update(notification)

    def pending(self):
        """Returns notifications with status PENDING"""

        return self.storage.pending(self.user_id)

    def created(self):
        """Returns notifications with status CREATED"""

        return self.storage.created(self.user_id)

    def shown(self):
        """Returns notifications with status SHOWN"""

        return self.storage.shown(self.user_id)

    def process_notifications(self):
        """Changes notification status from CREATED to PENDING if it's time to show notification"""

        self.storage.process_notifications()
