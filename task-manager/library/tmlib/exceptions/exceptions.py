class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidTaskTimeError(Error):
    """Exception that informs that task's start time greater than end time"""

    def __init__(self, start_time, end_time):
        super().__init__(
            'Start time {} greater than end time {}'.format(
                start_time, end_time))


class InvalidTaskPlanIntervalError(Error):
    """Exception that informs that task plan has too short interval (less than 5 minutes)"""

    def __init__(self, interval):
        super().__init__('Interval should be more than 5 minutes (300 seconds). Your interval is {} seconds'.format(interval))


class TaskDoesNotExistError(Error):
    def __init__(self):
        super().__init__('Task does not exist')


class UserHasNoRightError(Error):
    def __init__(self):
        super().__init__('User has no right for this action')
