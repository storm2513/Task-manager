from config.session import *
from enums.priority import Priority
from enums.status import Status
from models.task import Task
from config.logger import *
from config.config_parser import *

logger = init_logger('commands')


def login_user(email, password):
    user = Controllers.USERS.get_by_email(email)
    logger.debug('Got user')
    if user.password == password:
        logger.info('User authorized')
        write_user_to_config(user)
        Global.USER = user
    else:
        logger.debug(
            'Current password: {}, password: {}'.format(
                user.password, password))
        logger.warn('Wrong password')


def add_user(user):
    logger.info(
        "Added user with email: {}, name: {}, password:{}".format(
            user.email,
            user.name,
            user.password))
    Controllers.USERS.create(user)
    write_user_to_config(user)


def logout_user():
    remove_user_from_config()
    logger.info('User logged out')


def current_user():
    return Global.USER


def get_user_email_by_id(user_id):
    return Controllers.USERS.get_by_id(user_id).email


def get_level_by_user_id(user_id):
    return Controllers.LEVELS.get_by_user_id(user_id)


def update_user(user):
    Controllers.USERS.update(user)
    write_user_to_config(user)


def all_users():
    return Controllers.USERS.all()


def add_task(task):
    Controllers.TASKS.create(task)
    logger.info('Added task')


def update_task(task):
    if user_can_write_task(Global.USER.id, task.id):
        Controllers.TASKS.update(task)
    else:
        logger.info('User has no rights')


def get_task_by_id(task_id):
    if user_can_read_task(Global.USER.id, task_id):
        return Controllers.TASKS.get_by_id(task_id)
    else:
        return None


def delete_task(task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.delete(task_id)
    else:
        logger.info('User has no rights')


def create_inner_task(parent_task_id, task):
    if user_can_write_task(Global.USER.id, task.id):
        Controllers.TASKS.create_inner_task(parent_task_id, task)
    else:
        logger.info('User has no rights')


def get_inner_tasks(task_id):
    if user_can_read_task(Global.USER.id, task_id):
        return Controllers.TASKS.inner(task_id)
    else:
        logger.info('User has no rights')
        return None


def get_parent_task(task_id):
    return get_task_by_id(get_task_by_id(task_id).parent_task_id)


def assign_task_on_user(task_id, user_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.assign_task_on_user(task_id, user_id)
    else:
        logger.info('User has no rights')


def add_user_for_read(user_id, task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.add_user_for_read(user_id, task_id)
    else:
        logger.info('User has no rights')


def add_user_for_write(user_id, task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.add_user_for_write(user_id, task_id)
    else:
        logger.info('User has no rights')


def remove_user_for_read(user_id, task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.remove_user_for_read(user_id, task_id)
    else:
        logger.info('User has no rights')


def remove_user_for_write(user_id, task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.remove_user_for_write(user_id, task_id)
    else:
        logger.info('User has no rights')


def remove_user_for_read(user_id, task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.remove_user_for_read(user_id, task_id)
    else:
        logger.info('User has no rights')


def remove_user_for_write(user_Id, task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.remove_user_for_write(user_id, task_id)
    else:
        logger.info('User has no rights')


def user_tasks():
    return Controllers.TASKS.user_tasks(Global.USER.id)


def assigned_tasks():
    return Controllers.TASKS.assigned(Global.USER.id)


def can_read_tasks():
    return Controllers.TASKS.can_read(Global.USER.id)


def can_write_tasks():
    return Controllers.TASKS.can_write(Global.USER.id)


def tasks_with_status(status):
    return Controllers.TASKS.with_status(Global.USER.id, status)


def set_task_as_to_do(task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_to_do(task_id)
    else:
        logger.info('User has no rights')


def set_task_as_in_progress(task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_in_progress(task_id)
    else:
        logger.info('User has no rights')


def set_task_as_done(task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_done(task_id)
    else:
        logger.info('User has no rights')


def set_task_as_archived(task_id):
    if user_can_write_task(Global.USER.id, task_id):
        Controllers.TASKS.set_as_archived(task_id)
    else:
        logger.info('User has no rights')


def add_category(category):
    Controllers.CATEGORIES.create(category, Global.USER.id)
    logger.info('Category {} added'.format(category.name))


def all_categories():
    return Controllers.CATEGORIES.all(Global.USER.id)


def update_category(category):
    category = Controllers.CATEGORIES.get_by_id(category_id)
    if category.user_id == Global.USER.id:
        Controllers.CATEGORIES.update(category)
    else:
        logger.info('User has no rights')


def get_category_by_id(category_id):
    return Controllers.CATEGORIES.get_by_id(category_id)


def delete_category(category_id):
    category = Controllers.CATEGORIES.get_by_id(category_id)
    if category.user_id == Global.USER.id:
        Controllers.CATEGORIES.delete(category_id)


def user_can_read_task(user_id, task_id):
    task = Controllers.TASKS.get_by_id(task_id)
    if task is not None:
        return task.user_id == user_id or \
            task.assigned_user_id == user_id or \
            Controllers.TASKS.user_can_read(user_id, task_id) or \
            Controllers.TASKS.user_can_write(user_id, task_id)
    else:
        return None


def user_can_write_task(user_id, task_id):
    task = Controllers.TASKS.get_by_id(task_id)
    if task is not None:
        return task.user_id == user_id or \
            task.assigned_user_id == user_id or \
            Controllers.TASKS.user_can_write(user_id, task_id)
    else:
        return None
