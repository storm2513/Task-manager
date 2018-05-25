import enum


class NotificationStatus(enum.Enum):
    """
    Enum that stores values of notification's statuses
    CREATED - Notification was created
    PENDING - Notification should be shown
    SHOWN - Notification was shown
    """

    CREATED = 0
    PENDING = 1
    SHOWN = 2
