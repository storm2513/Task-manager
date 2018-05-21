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
        logger.debug('Current password: {}, password: {}'.format(user.password, password))
        logger.warn('Wrong password')

def add_user(user):
    logger.info("Added user with email: {}, name: {}, password:{}".format(user.email, user.name, user.password))
    Controllers.USERS.create(user)
    write_user_to_config(user)

def logout_user():
    remove_user_from_config()
    logger.info('User logged out')

def current_user():
    return Global.USER

def update_user(user):
    Controllers.USERS.update(user)
    write_user_to_config(user)

def all_users():
    return Controllers.USERS.all()

def add_task(task):
    Controllers.TASKS.create(task)
    logger.info('Added task')

def update_task(task):
    Controllers.TASKS.update(task)

def get_task_by_id(task_id):
    return Controllers.TASKS.get_by_id(task_id)

def delete_task(task_id):
    Controllers.TASKS.delete(task_id)

def change_task_status(task, status):
    Controllers.TASKS.change_status(task, status)

def create_inner_task(parent_task_id, task):
    Controllers.TASKS.create_inner_task(parent_task_id, task)

def get_inner_tasks(task_id):
    return Controllers.TASKS.inner(task_id)

def assign_task_on_user(user_id):
    Controllers.TASKS.assign_task_on_user(task_id, user_id)

def add_user_for_read(task_id):
    Controllers.TASKS.add_user_for_read(user_id, task_id)

def add_user_for_write(task_id):
    Controllers.TASKS.add_user_for_write(user_id, task_id)

def remove_user_for_read(task_id):
    Controllers.TASKS.remove_user_for_read(user_id, task_id)

def remove_user_for_write(task_id):
    Controllers.TASKS.remove_user_for_write(user_id, task_id)

def user_tasks():
    return Controllers.TASKS.user_tasks(Global.USER.id)

def set_task_as_to_do(task_id):
    Controllers.TASKS.set_as_to_do(task_id)

def set_task_as_in_progress(task_id):
    Controllers.TASKS.set_as_in_progress(task_id)

def set_task_as_done(task_id):
    Controllers.TASKS.set_as_done(task_id)

def set_task_as_archived(task_id):
    Controllers.TASKS.set_as_archived(task_id)

def add_category(category):
    Controllers.CATEGORIES.create(category, Global.USER.id)
    logger.info('Category {} added'.format(category.name))

def all_categories():
    return Controllers.CATEGORIES.all(Global.USER.id)

def update_category(category):
    Controllers.CATEGORIES.update(category)

def get_category_by_id(category_id):
    return Controllers.CATEGORIES.get_by_id(category_id)

def delete_category(category_id):
    Controllers.CATEGORIES.delete(category_id)
