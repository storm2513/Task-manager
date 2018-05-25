import enum


class Priority(enum.Enum):
    """
    Enum that stores values of task's priorities
    """

    MIN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    MAX = 4
