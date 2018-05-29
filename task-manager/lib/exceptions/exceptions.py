class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidEmailError(Error):
    """Exception that informs that email is invalid"""

    def __init__(self, email):
        super().__init__('Invalid email: {}'.format(email))
        self.email = email


class UserAlreadyExistsError(Error):
    """Exception that informs that user already exists"""

    def __init__(self, email):
        super().__init__('User with email "{}" already exists'.format(email))
        self.email = email


class UserDoesNotExistError(Error):
    """Exception that informs that user does not exists"""

    def __init__(self):
        super().__init__('User does not exist')


class IncorrectPasswordError(Error):
    """Exception that informs that user's password is incorrect"""

    def __init__(self, password):
        super().__init__('Password "{}" is incorrect'.format(password))
        self.password = password


class InvalidTaskTimeError(Error):
    """Exception that informs that task's start time greater than end time"""

    def __init__(self, start_time, end_time):
        super().__init__('Start time {} greater than end time {}'.format(start_time, end_time))
        self.password = password


class InvalidTaskPlanIntervalError(Error):
    """Exception that informs that task plan has too short interval (less than 5 minutes)"""

    def __init__(self, interval):
        super().__init__('Interval should be more than 5 minutes (300 seconds). Your interval is {} seconds'.format(interval))
        self.password = password


class TaskDoesNotExistError(Error):
    """Exception that informs that task does not exist"""

    def __init__(self):
        super().__init__('Task does not exist')


class UserHasNoRightError(Error):
    """Exception that informs that user has no right for this action"""

    def __init__(self):
        super().__init__('User has no right for this action')
