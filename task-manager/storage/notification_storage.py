from storage.storage_models import Notification, Task
from models.notification import Notification as NotificationInstance
from enums.notification_status import NotificationStatus
import datetime
from peewee import *


class NotificationStorage:
    """
    Class for managing notifications in database
    """

    def create(self, notification):
        """
        Creates notification
        """

        return self.to_notification_instance(
            Notification.create(
                id=notification.id,
                title=notification.title,
                user_id=notification.user_id,
                task_id=notification.task_id,
                status=notification.status,
                relative_start_time=notification.relative_start_time))

    def delete_by_id(self, notification_id):
        """
        Deletes notification by ID
        """

        Notification.delete().where(Notification.id == notification_id).execute()

    def update(self, notification):
        """
        Updates notification title, status and relative_start_time
        """

        Notification.update(
            title=notification.title,
            status=notification.status,
            relative_start_time=notification.relative_start_time).where(
            Notification.id == notification.id).execute()

    def to_notification_instance(self, notification):
        """
        Makes cast from Notification class to NotificationInstance class
        """

        return NotificationInstance(
            id=notification.id,
            title=notification.title,
            user_id=notification.user_id,
            task_id=notification.task_id,
            status=notification.status,
            relative_start_time=notification.relative_start_time)

    def get_by_id(self, notification_id):
        """
        Returns notification by it's ID
        """

        try:
            return self.to_notification_instance(
                Notification.get(Notification.id == notification_id))
        except DoesNotExist:
            return None

    def pending(self, user_id):
        """
        Returns notifications with PENDING status for user with ID == user_id
        """

        return list(map(self.to_notification_instance,
                        list(Notification.select().where(Notification.user_id == user_id,
                                                         Notification.status == NotificationStatus.PENDING.value))))

    def created(self, user_id):
        """
        Returns notifications with CREATED status for user with ID == user_id
        """

        return list(map(self.to_notification_instance,
                        list(Notification.select().where(Notification.user_id == user_id,
                                                         Notification.status == NotificationStatus.CREATED.value))))

    def shown(self, user_id):
        """
        Returns notifications with SHOWN status for user with ID == user_id
        """

        return list(map(self.to_notification_instance,
                        list(Notification.select().where(Notification.user_id == user_id,
                                                         Notification.status == NotificationStatus.SHOWN.value))))

    def all_user_notifications(self, user_id):
        """
        Returns all user's notifications
        """

        return list(map(self.to_notification_instance, list(
            Notification.select().where(Notification.user_id == user_id))))

    def process_notifications(self):
        """
        Changes notification status from CREATED to PENDING if it's time to show notification
        """

        for notification in Notification.select().where(
                Notification.status == NotificationStatus.CREATED.value).join(Task).where(
                Task.id == Notification.task_id):
            task = Task.get(Task.id == notification.task_id)
            if task.start_time - \
                    datetime.timedelta(seconds=notification.relative_start_time) < datetime.datetime.now():
                notification.status = NotificationStatus.PENDING.value
                notification.save()
