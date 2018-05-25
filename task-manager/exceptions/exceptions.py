class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidEmailError(Error):
    def __init__(self, email):
        super().__init__('Invalid email: {}'.format(email))
        self.email = email


class UserAlreadyExistsError(Error):
    def __init__(self, email):
        super().__init__('User with email "{}" already exists'.format(email))
        self.email = email


class UserDoesNotExistError(Error):
    def __init__(self):
        super().__init__('User does not exist')


class IncorrectPasswordError(Error):
    def __init__(self, password):
        super().__init__('Password "{}" is incorrect'.format(password))
        self.password = password


class InvalidTaskTimeError(Error):
    def __init__(self, start_time, end_time):
        super().__init__('Start time {} greater than end time {}'.format(start_time, end_time))
        self.password = password


class InvalidTaskPlanIntervalError(Error):
    def __init__(self, interval):
        super().__init__('Interval should be more than 5 minutes (300 seconds). Your interval is {} seconds'.format(interval))
        self.password = password


class TaskDoesNotExistError(Error):
    def __init__(self):
        super().__init__('Task does not exist')


class UserHasNoRightError(Error):
    def __init__(self):
        super().__init__('User has no right for this action')
