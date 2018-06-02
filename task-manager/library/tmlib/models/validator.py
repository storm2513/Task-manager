from tmlib.exceptions.exceptions import InvalidTaskTimeError, InvalidTaskPlanIntervalError
import dateparser


def validate_start_time_less_than_end_time(start_time, end_time):
    """
    Validates that start_time is less than end_time. Otherwise raises exception
    """

    if start_time is not None and end_time is not None:
        if start_time > end_time:
            raise InvalidTaskTimeError(start_time, end_time)


def validate_task_plan_interval(interval):
    """
    Validates that task plan interval is more than 5 minutes. Otherwise raises exception
    """

    if interval < 300:  # 5 minutes
        raise InvalidTaskPlanIntervalError(interval)


def validate_task(task):
    """
    Validates task's fields
    """

    validate_start_time_less_than_end_time(task.start_time, task.end_time)


def validate_task_plan(plan):
    """
    Validates task plan's fields
    """

    validate_task_plan_interval(plan.interval)