import re
from exceptions.exceptions import *
import dateparser


def validate_email(email):
    """
    Validates email and raises exception if it doesn't match to the regex
    pattern. More about this regex you can read at http://emailregex.com/
    """
    EMAIL_PATTERN = (r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

    if re.match(EMAIL_PATTERN, email) is None:
        raise InvalidEmailError(email)


def validate_start_time_less_than_end_time(start_time, end_time):
    if start_time is not None and end_time is not None:
        if start_time > end_time:
            raise InvalidTaskTimeError(start_time, end_time)

def validate_task_plan_interval(interval):
    if interval < 300: # 5 minutes
        raise InvalidTaskPlanIntervalError(interval)

def validate_user(user):
    validate_email(user.email)


def validate_task(task):
    validate_start_time_less_than_end_time(task.start_time, task.end_time)


def validate_task_plan(plan):
    validate_task_plan_interval(plan.interval)

