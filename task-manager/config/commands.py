from config.session import *
from enums.priority import Priority
from enums.status import Status
from models.task import Task

def login(email, password):
    user = Controllers.USERS.get_by_email(email)
    if user.password == password:
        Global.USER = user

def register(email, name, password):
    user = User(email=email, name=name, password=password)
    Global.USER = Controllers.USERS.create(user)

def add_task(task):
    Controllers.TASKS.create(task)

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

def assign_task_on_user(task_id, user_id):
    Controllers.TASKS.assign_task_on_user(task_id, user_id)

def add_user_for_read(user_id, task_id):
    Controllers.TASKS.add_user_for_read(user_id, task_id)

def add_user_for_write(user_id, task_id):
    Controllers.TASKS.add_user_for_write(user_id, task_id)

def remove_user_for_read(user_id, task_id):
    Controllers.TASKS.remove_user_for_read(user_id, task_id)

def remove_user_for_write(user_id, task_id):
    Controllers.TASKS.remove_user_for_write(user_id, task_id)

def get_user_tasks(self):
    return Controllers.TASKS.user_tasks(Global.USER.id)

def set_task_as_to_do(self, task_id):
    Controllers.TASKS.set_as_to_do(task_id)

def set_task_as_in_progress(self, task_id):
    Controllers.TASKS.set_as_in_progress(task_id)

def set_task_as_done(self, task_id):
    Controllers.TASKS.set_as_done(task_id)

def set_task_as_archived(self, task_id):
    Controllers.TASKS.set_as_archived(task_id)

def create_category(self, category):
    Controllers.CATEGORIES.create(category, Global.USER.id)

def update_category(self, category):
    Controllers.CATEGORIES.update(category)

def delete_category(self, category_id):
    Controllers.CATEGORIES.delete(category_id)
