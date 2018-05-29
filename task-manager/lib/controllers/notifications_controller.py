from lib.storage.notification_storage import NotificationStorage
from lib.models.notification import Status as NotificationStatus


class NotificationsController:
    """
    Class for managing notifications
    """

    def __init__(self, notification_storage):
        """
        Storage field for access to database
        """

        self.notification_storage = notification_storage

    def create(self, notification, user_id):
        """
        Creates notification
        """

        notification.user_id = user_id
        return self.notification_storage.create(notification)

    def update(self, notification):
        """
        Updates notification
        """

        self.notification_storage.update(notification)

    def delete(self, notification_id):
        """
        Deletes notification by ID
        """

        self.notification_storage.delete_by_id(notification_id)

    def get_by_id(self, notification_id):
        """
        Returns notification by ID
        """

        return self.notification_storage.get_by_id(notification_id)

    def all(self, user_id):
        """
        Returns all user notifications
        """

        return self.notification_storage.all_user_notifications(user_id)

    def set_as_shown(self, notification_id):
        """
        Sets notification's status with ID == notification_id as SHOWN
        """

        notification = self.get_by_id(notification_id)
        notification.status = NotificationStatus.SHOWN.value
        self.update(notification)

    def pending(self, user_id):
        """
        Returns notifications with status PENDING
        """

        return self.notification_storage.pending(user_id)

    def created(self, user_id):
        """
        Returns notifications with status CREATED
        """

        return self.notification_storage.created(user_id)

    def shown(self, user_id):
        """
        Returns notifications with status SHOWN
        """

        return self.notification_storage.shown(user_id)

    def process_notifications(self):
        """
        Changes notification status from CREATED to PENDING if it's time to show notification
        """

        self.notification_storage.process_notifications()
