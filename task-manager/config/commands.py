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
    Controllers.TASKS.get_by_id(task_id)

def delete_task(task_id):
    Controllers.TASKS.delete(task_id)

def change_task_status(task, status):
    Controllers.TASKS.change_status(task, status)

def create_inner_task(parent_task_id, task):
    Controllers.TASKS.create_inner_task(parent_task_id, task)

def assign_user_on_task(user_id, task):
    Controllers.TASKS.assign_user_on_task(user_id, task)

def add_user_for_read(user_id, task_id):
    Controllers.TASKS.add_user_for_read(user_id, task_id)

def add_user_for_write(user_id, task_id):
    Controllers.TASKS.add_user_for_write(user_id, task_id)

def remove_user_for_read(user_id, task_id):
    Controllers.TASKS.add_user_for_read(user_id, task_id)

def remove_user_for_write(user_id, task_id):
    Controllers.TASKS.add_user_for_write(user_id, task_id)

def get_user_tasks(user=Global.USER):
    return Controllers.TASKS.user_tasks(Global.USER)

def set_task_as_to_do(self, task):
    Controllers.TASKS.set_as_to_do(task)

def set_task_as_in_progress(self, task):
    Controllers.TASKS.set_as_in_progress(task)

def set_task_as_complete(self, task):
    Controllers.TASKS.set_as_complete(task)

def set_task_as_archive(self, task):
    Controllers.TASKS.set_as_archive(task)

def create_category(self, category):
    Controllers.CATEGORIES.create(category, Global.USER.id)

def update_category(self, category):
    Controllers.CATEGORIES.update(category)

def delete_category(self, category_id):
    Controllers.CATEGORIES.delete(category_id)