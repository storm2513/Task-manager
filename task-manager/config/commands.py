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

def delete_task(task_id):
    Controllers.TASKS.delete(task_id)

def tasks(user=Global.USER):
    return Controllers.TASKS.user_tasks(Global.USER)
