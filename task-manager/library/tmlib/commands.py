"""This module provides all methods to work with library"""


from tmlib.models.task import Task, Status
from tmlib.models.validator import validate_task, validate_task_plan
from tmlib.exceptions.exceptions import UserHasNoRightError, TaskDoesNotExistError
import tmlib.logger as log


def add_task(tasks_controller, task):
    validate_task(task)
    log.get_logger().info('Added task')
    return tasks_controller.create(task)


def add_task_plan(task_plans_controller, plan):
    validate_task_plan(plan)
    log.get_logger().info('Added task plan')
    task_plans_controller.create(plan)


def get_task_plan_by_id(task_plans_controller, plan_id):
    return task_plans_controller.get_by_id(plan_id)


def get_task_plans(task_plans_controller):
    return task_plans_controller.all()


def get_tasks_created_by_task_plan(tasks_controller, plan_id):
    return tasks_controller.created_by_task_plan(plan_id)


def update_task(tasks_controller, task):
    validate_task(task)
    if user_can_write_task(tasks_controller, task.id):
        tasks_controller.update(task)
        log.get_logger().info('Updated task')
    else:
        log.get_logger().error(
            'User has no rights for updating task')
        raise UserHasNoRightError


def update_task_plan(task_plans_controller, plan):
    validate_task_plan(plan)
    task_plans_controller.update(plan)
    log.get_logger().info('Updated task plan')


def get_task_by_id(tasks_controller, task_id):
    if user_can_read_task(tasks_controller, task_id):
        return tasks_controller.get_by_id(task_id)
    else:
        return None


def delete_task(tasks_controller, task_id):
    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.delete(task_id)
        log.get_logger().info(
            'Deleted task with ID {}'.format(task_id))
    else:
        log.get_logger().error(
            'User has no right for deleting task')
        raise UserHasNoRightError


def delete_task_plan(task_plans_controller, task_plan_id):
    task_plans_controller.delete(task_plan_id)
    log.get_logger().info(
        'Deleted task plan with ID {}'.format(task_plan_id))


def create_inner_task(tasks_controller, parent_task_id, task):
    """Checks if parent task exists, then creates inner task"""

    parent_task = get_task_by_id(tasks_controller, parent_task_id)
    if parent_task is None:
        log.get_logger().error('Task does not exist')
        raise TaskDoesNotExistError
    validate_task(task)
    if user_can_write_task(tasks_controller, parent_task_id):
        tasks_controller.create_inner_task(parent_task_id, task)
        log.get_logger().info(
            'Created inner task for task with ID: {}'.format(task.id))
    else:
        log.get_logger().error(
            'User has no right for creating inner task')
        raise UserHasNoRightError


def filter_tasks(tasks_controller, *args):
    """
    Before usage you should import Task from tmlib.storage.storage_models module.
    Then you can pass 2 arguments: tasks_controller and filter query.
    If you want to filter multiple fields use bitwise operators (& and |) rather than logical operators (and and or).

    Example:
    filter_tasks(
        controller,
        Task.title.contains('title') & Task.created_at > datetime.datetime.now())
    """

    return tasks_controller.filter(args)


def get_inner_tasks(tasks_controller, task_id, recursive=False):
    """Returns inner tasks for task with ID == task_id"""

    if user_can_read_task(tasks_controller, task_id):
        return tasks_controller.inner(task_id, recursive)
    else:
        log.get_logger().error(
            'User has no right for getting inner task')
        raise UserHasNoRightError


def get_parent_task(tasks_controller, task_id):
    """Returns parent task for task with ID == task_id"""

    task = get_task_by_id(tasks_controller, task_id)
    if task is not None and task.parent_task_id is not None:
        return get_task_by_id(tasks_controller, task.parent_task_id)


def assign_task_on_user(tasks_controller, task_id, user_id):
    """Assigns task with ID == task_id on user with ID == user_id"""

    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.assign_task_on_user(task_id, user_id)
        log.get_logger().info(
            'Assigned task with ID: {} on user with ID: {}'.format(
                task_id, user_id))
    else:
        log.get_logger().error(
            'User has no right for assigning this task')
        raise UserHasNoRightError


def add_user_for_read(tasks_controller, user_id, task_id):
    """Allows user with ID == user_id to read task with ID == task_id"""

    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.add_user_for_read(user_id, task_id)
        log.get_logger().info(
            'Gave user with ID: {} read access to task with ID: {}'.format(
                user_id, task_id))
    else:
        log.get_logger().error(
            'User has no right for giving access for this task')
        raise UserHasNoRightError


def add_user_for_write(tasks_controller, user_id, task_id):
    """Allows user with ID == user_id to read and change task with ID == task_id"""

    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.add_user_for_write(user_id, task_id)
        log.get_logger().info(
            'Gave user with ID: {} read and write access to task with ID: {}'.format(
                user_id, task_id))
    else:
        log.get_logger().error(
            'User has no right for giving access for this task')
        raise UserHasNoRightError


def remove_user_for_read(tasks_controller, user_id, task_id):
    """Removes permission to read task with ID == task_id from user with ID == user_id"""

    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.remove_user_for_read(user_id, task_id)
        log.get_logger().info(
            'Removed from user with ID: {} read access to task with ID: {}'.format(
                user_id, task_id))
    else:
        log.get_logger().error(
            'User has no right for removing access for this task')
        raise UserHasNoRightError


def remove_all_users_for_read(tasks_controller, task_id):
    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.remove_all_users_for_read(task_id)
        log.get_logger().info(
            'Removed read access to task with ID: {} for all users'.format(task_id))
    else:
        log.get_logger().error(
            'User has no right for removing access for this task')
        raise UserHasNoRightError


def remove_user_for_write(tasks_controller, user_id, task_id):
    """Removes permission to read and change task with ID == task_id from user with ID == user_id"""

    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.remove_user_for_write(user_id, task_id)
        log.get_logger().info(
            'Removed from user with ID: {} read and write access to task with ID: {}'.format(
                user_id, task_id))
    else:
        log.get_logger().error(
            'User has no right for removing access for this task')
        raise UserHasNoRightError


def remove_all_users_for_write(tasks_controller, task_id):
    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.remove_all_users_for_write(task_id)
        log.get_logger().info(
            'Removed read and write access to task with ID: {} for all users'.format(task_id))
    else:
        log.get_logger().error(
            'User has no right for removing access for this task')
        raise UserHasNoRightError


def get_users_can_read_task(tasks_controller, task_id):
    return tasks_controller.get_users_can_read_task(task_id)


def get_users_can_write_task(tasks_controller, task_id):
    return tasks_controller.get_users_can_write_task(task_id)


def user_tasks(tasks_controller):
    return tasks_controller.user_tasks()


def assigned_tasks(tasks_controller):
    return tasks_controller.assigned()


def can_read_tasks(tasks_controller):
    return tasks_controller.can_read()


def can_write_tasks(tasks_controller):
    return tasks_controller.can_write()


def tasks_with_status(tasks_controller, status):
    return tasks_controller.with_status(status)


def set_task_status(tasks_controller, task_id, status):
    if user_can_write_task(tasks_controller, task_id):
        tasks_controller.set_status(task_id, status)
        log.get_logger().info(
            "Set task's status with ID {} as {}".format(
                task_id, Status(status).name))
    else:
        log.get_logger().error(
            'User has no right for changing status for this task')
        raise UserHasNoRightError


def add_category(categories_controller, category):
    categories_controller.create(category)
    log.get_logger().info(
        'Category {} added'.format(category.name))


def user_categories(categories_controller):
    return categories_controller.all()


def update_category(categories_controller, category):
    if categories_controller.get_by_id(
            category.id).user_id == categories_controller.user_id:
        categories_controller.update(category)
    else:
        log.get_logger().error('User has no rights')
        raise UserHasNoRightError


def get_category_by_id(categories_controller, category_id):
    return categories_controller.get_by_id(category_id)


def delete_category(categories_controller, category_id):
    category = categories_controller.get_by_id(category_id)
    if category.user_id == categories_controller.user_id:
        categories_controller.delete(category_id)
        log.get_logger().info('Deleted category')


def user_can_read_task(tasks_controller, task_id):
    task = tasks_controller.get_by_id(task_id)
    if task is not None:
        return (task.user_id == tasks_controller.user_id or
                task.assigned_user_id == tasks_controller.user_id or
                tasks_controller.user_can_read(task_id) or
                tasks_controller.user_can_write(task_id))


def user_can_write_task(tasks_controller, task_id):
    task = tasks_controller.get_by_id(task_id)
    if task is not None:
        return (task.user_id == tasks_controller.user_id or
                task.assigned_user_id == tasks_controller.user_id or
                tasks_controller.user_can_write(task_id))


def add_notification(tasks_controller, notifications_controller, notification):
    task = get_task_by_id(tasks_controller, notification.task_id)
    if task is None:
        log.get_logger().error('Task does not exist')
        raise TaskDoesNotExistError
    notifications_controller.create(notification)
    log.get_logger().info('Created notification')


def get_notification_by_id(notifications_controller, notification_id):
    return notifications_controller.get_by_id(notification_id)


def delete_notification(notifications_controller, notification_id):
    notifications_controller.delete(notification_id)
    log.get_logger().info('Deleted notification')


def user_notifications(notifications_controller):
    return notifications_controller.all()


def update_notification(
        tasks_controller,
        notifications_controller,
        notification):
    task = get_task_by_id(tasks_controller, notification.task_id)
    if task is None:
        log.get_logger().error('Task does not exist')
        raise TaskDoesNotExistError
    notifications_controller.update(notification)
    log.get_logger().info('Updated notification')


def pending_notifications(notifications_controller):
    return notifications_controller.pending()


def user_created_notifications(notifications_controller):
    return notifications_controller.created()


def user_shown_notifications(notifications_controller):
    return notifications_controller.shown()


def set_notification_as_shown(notifications_controller, notification_id):
    """Sets notification's status with ID == notification_id as SHOWN"""

    notifications_controller.set_as_shown(notification_id)
    log.get_logger().info(
        "Set notification's status with ID {} as SHOWN".format(notification_id))
