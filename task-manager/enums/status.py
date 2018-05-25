import enum


class Status(enum.Enum):
    """
    Enum that stores values of task's statuses
    """

    TODO = 0
    IN_PROGRESS = 1
    DONE = 2
    ARCHIVED = 3
    TEMPLATE = 4
