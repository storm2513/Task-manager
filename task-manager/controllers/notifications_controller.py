from storage.notification_storage import NotificationStorage
from enums.notification_status import NotificationStatus


class NotificationsController:
    def __init__(self, notification_storage):
        self.notification_storage = notification_storage

    def create(self, notification, user_id):
        notification.user_id = user_id
        return self.notification_storage.create(notification)

    def update(self, notification):
        self.notification_storage.update(notification)

    def delete(self, notification_id):
        self.notification_storage.delete_by_id(notification_id)

    def get_by_id(self, notification_id):
        return self.notification_storage.get_by_id(notification_id)

    def all(self, user_id):
        return self.notification_storage.all_user_notifications(user_id)

    def set_as_shown(self, notification_id):
        notification = self.get_by_id(notification_id)
        notification.status = NotificationStatus.SHOWN.value
        self.update(notification)

    def pending(self, user_id):
        return self.notification_storage.pending(user_id)

    def created(self, user_id):
        return self.notification_storage.created(user_id)

    def shown(self, user_id):
        return self.notification_storage.shown(user_id)

    def process_notifications(self):
        self.notification_storage.process_notifications()
