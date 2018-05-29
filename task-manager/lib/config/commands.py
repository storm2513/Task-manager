from lib.config.session import *
from lib.models.task import Task, Status, Priority
from lib.models.validator import *
import lib.config.logger as logging
from lib.config.config_parser import *


"""
This module provides all methods to work with library
"""

_log_tag = 'Commands'


def login_user(email, password):
    """
    Authorizes user by email and password.
    Writes user's email and password to config file.
    Raises errors if user doesn't exist or password is incorrect
    """

    user = Controllers.USERS.get_by_email(email)
    if user is not None:
        logging.get_logger(_log_tag).debug(
            'Got user from db by email')
        if user.password == password:
            write_user_to_config(user)
            logging.get_logger(_log_tag).debug(
                'User authorized')
            Global.USER = user
        else:
            logging.get_logger(_log_tag).error(
                'Wrong password')
            raise IncorrectPasswordError(password)
    else:
        logging.get_logger(_log_tag).error(
            'User does not exist')
        raise UserDoesNotExistError


def add_user(user):
    """
    Adds user. Checks if user with such email already exists.
    Writes registered user to config
    """

    validate_user(user)
    if Controllers.USERS.get_by_email(user.email) is not None:
        logging.get_logger(_log_tag).error(
            'User already exists')
        raise UserAlreadyExistsError(user.email)
    else:
        logging.get_logger(_log_tag).info(
            "Added user with email: {}, name: {}, password:{}".format(
                user.email,
                user.name,
                user.password))
        Controllers.USERS.create(user)
        write_user_to_config(user)


def logout_user():
    """
    Removes user from config
    """

    remove_user_from_config()
    logging.get_logger(_log_tag).info('User logged out')


def current_user():
    """
    Returns current user
    """

    return Global.USER


def get_user_email_by_id(user_id):
    """
    Returns user's email by it's ID
    """

    user = Controllers.USERS.get_by_id(user_id)
    if user is None:
        logging.get_logger(_log_tag).error('User does not exist')
        raise UserDoesNotExistError
    return user.email


def get_level_by_user_id(user_id):
    """
    Returns user's level by user's ID
    """

    return Controllers.LEVELS.get_by_user_id(user_id)


def update_user(user):
    """
    Updates user
    """

    validate_user(user)
    logging.get_logger(_log_tag).info('Updated user')
    Controllers.USERS.update(user)
    write_user_to_config(user)


def all_users():
    """
    Returns list of all users without passwords
    """

    return Controllers.USERS.all()


def add_task(task):
    """
    Adds task
    """

    validate_task(task)
    return Controllers.TASKS.create(task)
    logging.get_logger(_log_tag).info('Added task')


def add_task_plan(plan):
    """
    Adds task plan
    """

    validate_task_plan(plan)
    Controllers.TASK_PLANS.create(plan)
    logging.get_logger(_log_tag).info('Added task plan')


def get_task_plan_by_id(plan_id):
    """
    Returns task plan by it's ID
    """

    return Controllers.TASK_PLANS.get_by_id(plan_id)


def get_task_plans():
    """
    Returns all task plans for user
    """

    return Controllers.TASK_PLANS.all(Global.USER.id)


def update_task(task):
    """
    Updates task
    """

    validate_task(task)
    if user_can_write_task(Global.USER.id, task.id):
        Controllers.TASKS.update(task)
        logging.get_logger(_log_tag).info('Updated task')
    else:
        logging.get_logger(_log_tag).error(
            'User has no rights for updating task')
        raise UserHasNoRightError


def update_task_plan(plan):
    """
    Updates task plan
    """

    validate_task_plan(plan)
    Controllers.TASK_PLANS.update(plan)
    logging.get_logger(_log_tag).info('Updated task plan')


def get_task_by_id(task_id):
    """
    Returns task by it's ID
    """

    if user_can_read_task(Global.USER.id, task_id):
        return Controllers.TASKS.get_by_id(task_id)
    else:
        return None


def delete_task(task_id):
    """
    Deletes task by it's ID
    """

    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.delete(task_id)
        logging.get_logger(_log_tag).info('Deleted task with ID {}'.format(task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for deleting task')
        raise UserHasNoRightError


def create_inner_task(parent_task_id, task):
    """
    Checks if parent task exists, then creates inner task
    """

    parent_task = get_task_by_id(parent_task)
    if parent_task is None:
        logging.get_logger(_log_tag).error('Task does not exist')
        raise TaskDoesNotExistError
    validate_task(task)
    if user_can_write_task(Global.USER.id, task.id):
        Controllers.TASKS.create_inner_task(parent_task_id, task)
        logging.get_logger(_log_tag).info(
            'Created inner task for task with ID: {}'.format(task.id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for creating inner task')
        raise UserHasNoRightError


def get_inner_tasks(task_id):
    """
    Returns inner tasks for task with ID == task_id
    """

    if user_can_read_task(Global.USER.id, task_id):
        return Controllers.TASKS.inner(task_id)
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for getting inner task')
        raise UserHasNoRightError


def get_parent_task(task_id):
    """
    Returns parent task for task with ID == task_id
    """

    task = get_task_by_id(task_id)
    if task is not None and task.parent_task_id is not None:
        return get_task_by_id(task.parent_task_id)


def validate_user_exists(user_id):
    """
    Validates that user exists. Otherwise raises exception
    """

    user = Controllers.USERS.get_by_id(user_id)
    if user is None:
        logging.get_logger(_log_tag).error('User does not exist')
        raise UserDoesNotExistError


def assign_task_on_user(task_id, user_id):
    """
    Assigns task with ID == task_id on user with ID == user_id
    """

    if user_can_write_task(Global.USER.id, task_id):
        validate_user_exists(user_id)
        Controllers.TASKS.assign_task_on_user(task_id, user_id)
        logging.get_logger(_log_tag).info(
            'Assigned task with ID: {} on user with ID: {}'.format(task_id, user_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for assigning this task')
        raise UserHasNoRightError


def add_user_for_read(user_id, task_id):
    """
    Allows user with ID == user_id to read task with ID == task_id
    """

    if user_can_write_task(Global.USER.id, task_id):
        validate_user_exists(user_id)
        Controllers.TASKS.add_user_for_read(user_id, task_id)
        logging.get_logger(_log_tag).info(
            'Gave user with ID: {} read access to task with ID: {}'.format(user_id, task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for giving access for this task')
        raise UserHasNoRightError


def add_user_for_write(user_id, task_id):
    """
    Allows user with ID == user_id to read and change task with ID == task_id
    """

    if user_can_write_task(Global.USER.id, task_id):
        validate_user_exists(user_id)
        Controllers.TASKS.add_user_for_write(user_id, task_id)
        logging.get_logger(_log_tag).info(
            'Gave user with ID: {} read and write access to task with ID: {}'.format(user_id, task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for giving access for this task')
        raise UserHasNoRightError


def remove_user_for_read(user_id, task_id):
    """
    Removes permission to read task with ID == task_id from user with ID == user_id
    """

    if user_can_write_task(Global.USER.id, task_id):
        validate_user_exists(user_id)
        Controllers.TASKS.remove_user_for_read(user_id, task_id)
        logging.get_logger(_log_tag).info(
            'Removed from user with ID: {} read access to task with ID: {}'.format(user_id, task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for removing access for this task')
        raise UserHasNoRightError


def remove_user_for_write(user_id, task_id):
    """
    Removes permission to read and change task with ID == task_id from user with ID == user_id
    """

    if user_can_write_task(Global.USER.id, task_id):
        validate_user_exists(user_id)
        Controllers.TASKS.remove_user_for_write(user_id, task_id)
        logging.get_logger(_log_tag).info(
            'Removed from user with ID: {} read and write access to task with ID: {}'.format(user_id, task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for removing access for this task')
        raise UserHasNoRightError


def user_tasks():
    """
    Returns all user's tasks
    """

    return Controllers.TASKS.user_tasks(Global.USER.id)


def assigned_tasks():
    """
    Returns assigned tasks for user
    """

    return Controllers.TASKS.assigned(Global.USER.id)


def can_read_tasks():
    """
    Returns tasks that user can read
    """

    return Controllers.TASKS.can_read(Global.USER.id)


def can_write_tasks():
    """
    Returns tasks that user can read and change
    """

    return Controllers.TASKS.can_write(Global.USER.id)


def tasks_with_status(status):
    """
    Returns user's tasks with provided status
    """

    return Controllers.TASKS.with_status(Global.USER.id, status)


def set_task_as_to_do(task_id):
    """
    Sets task's status as TODO by ID
    """

    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_to_do(task_id)
        logging.get_logger(_log_tag).info(
            "Set task's status with ID {} as TODO".format(task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for changing status for this task')
        raise UserHasNoRightError


def set_task_as_in_progress(task_id):
    """
    Sets task's status as IN_PROGRESS by ID
    """

    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_in_progress(task_id)
        logging.get_logger(_log_tag).info(
            "Set task's status with ID {} as IN_PROGRESS".format(task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for changing status for this task')
        raise UserHasNoRightError


def set_task_as_done(task_id):
    """
    Sets task's status as DONE by ID
    """

    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_done(task_id)
        logging.get_logger(_log_tag).info(
            "Set task's status with ID {} as DONE".format(task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for changing status for this task')
        raise UserHasNoRightError


def set_task_as_archived(task_id):
    """
    Sets task's status as ARCHIVED by ID
    """

    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_archived(task_id)
        logging.get_logger(_log_tag).info(
            "Set task's status with ID {} as ARCHIVED".format(task_id))
    else:
        logging.get_logger(_log_tag).error(
            'User has no right for changing status for this task')
        raise UserHasNoRightError


def add_category(category):
    """
    Adds category
    """

    Controllers.CATEGORIES.create(category, Global.USER.id)
    logging.get_logger(_log_tag).info(
        'Category {} added'.format(category.name))


def all_categories():
    """
    Returns all categories
    """

    return Controllers.CATEGORIES.all(Global.USER.id)


def update_category(category):
    """
    Updates category
    """

    if Controllers.CATEGORIES.get_by_id(category.id).user_id == Global.USER.id:
        Controllers.CATEGORIES.update(category)
    else:
        logging.get_logger(_log_tag).error('User has no rights')
        raise UserHasNoRightError


def get_category_by_id(category_id):
    """
    Returns category by it's ID
    """

    return Controllers.CATEGORIES.get_by_id(category_id)


def delete_category(category_id):
    """
    Deletes category by it's ID
    """

    category = Controllers.CATEGORIES.get_by_id(category_id)
    if category.user_id == Global.USER.id:
        Controllers.CATEGORIES.delete(category_id)
        logging.get_logger(_log_tag).info('Deleted category')


def user_can_read_task(user_id, task_id):
    """
    Returns True if user with ID == user_id can read task with ID == task_id
    """

    task = Controllers.TASKS.get_by_id(task_id)
    if task is not None:
        return task.user_id == user_id or \
            task.assigned_user_id == user_id or \
            Controllers.TASKS.user_can_read(user_id, task_id) or \
            Controllers.TASKS.user_can_write(user_id, task_id)
    else:
        return None


def user_can_write_task(user_id, task_id):
    """
    Returns True if user with ID == user_id can read and change task with ID == task_id
    """

    task = Controllers.TASKS.get_by_id(task_id)
    if task is not None:
        return task.user_id == user_id or \
            task.assigned_user_id == user_id or \
            Controllers.TASKS.user_can_write(user_id, task_id)
    else:
        return None


def add_notification(notification):
    """
    Adds notification
    """

    task = commands.get_task_by_id(notification.task_id)
    if task is None:
        logging.get_logger(_log_tag).error('Task does not exist')
        raise TaskDoesNotExistError
    Controllers.NOTIFICATIONS.create(notification, Global.USER.id)
    logging.get_logger(_log_tag).info('Created notification')


def get_notification_by_id(notification_id):
    """
    Returns notifications by ID
    """

    return Controllers.NOTIFICATIONS.get_by_id(notification_id)


def delete_notification(notification_id):
    """
    Deletes notification by ID
    """

    Controllers.NOTIFICATIONS.delete(notification_id)
    logging.get_logger(_log_tag).info('Deleted notification')


def user_notifications():
    """
    Returns all user's notifications
    """

    return Controllers.NOTIFICATIONS.all(Global.USER.id)


def update_notification(notification):
    """
    Updates notification
    """

    task = commands.get_task_by_id(notification.task_id)
    if task is None:
        logging.get_logger(_log_tag).error('Task does not exist')
        raise TaskDoesNotExistError
    Controllers.NOTIFICATIONS.update(notification)
    logging.get_logger(_log_tag).info('Updated notification')


def pending_notifications():
    """
    Returns notifications with status PENDING
    """

    return Controllers.NOTIFICATIONS.pending(Global.USER.id)


def user_created_notifications():
    """
    Returns notifications with status CREATED
    """

    return Controllers.NOTIFICATIONS.created(Global.USER.id)


def user_shown_notifications():
    """
    Returns notifications with status SHOWN
    """

    return Controllers.NOTIFICATIONS.shown(Global.USER.id)


def set_notification_as_shown(notification_id):
    """
    Sets notification's status with ID == notification_id as SHOWN
    """

    Controllers.NOTIFICATIONS.set_as_shown(notification_id)
    logging.get_logger(_log_tag).info(
        "Set notification's status with ID {} as SHOWN".format(notification_id))


def enable_logging(enabled):
    write_logging_status_to_config(enabled)
