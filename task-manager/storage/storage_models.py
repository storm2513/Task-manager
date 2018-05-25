from peewee import *
import datetime

from enums.status import Status
from enums.priority import Priority
from enums.notification_status import NotificationStatus

db = SqliteDatabase('task_manager.db')


class BaseModel(Model):
    """
    Base class for classes that work with peewee library
    """

    class Meta:
        database = db


class Level(BaseModel):
    """
    User's level model
    """

    id = PrimaryKeyField(null=False)
    experience = IntegerField(default=1)


class User(BaseModel):
    """
    User model
    """

    id = PrimaryKeyField(null=False)
    email = CharField()
    name = CharField()
    password = CharField()
    level = ForeignKeyField(Level, backref='user')


class Category(BaseModel):
    """
    Category model
    """

    id = PrimaryKeyField(null=False)
    name = CharField()
    user = ForeignKeyField(User, backref='categories')


class Task(BaseModel):
    """
    Task model
    """

    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='tasks', null=True)
    title = CharField()
    note = CharField(default="")
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    assigned_user = ForeignKeyField(User, null=True)
    parent_task_id = IntegerField(null=True)
    is_event = BooleanField(default=False)
    category = ForeignKeyField(Category, backref='tasks', null=True)
    priority = IntegerField(default=Priority.MEDIUM.value)
    status = IntegerField(default=Status.TODO.value)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Task, self).save(*args, **kwargs)


class TaskPlan(BaseModel):
    """
    TaskPlan model
    """

    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='task_plans', null=True)
    task = ForeignKeyField(Task, null=True)
    interval = IntegerField()
    last_created_at = DateTimeField()


class Notification(BaseModel):
    """
    Notification model
    """

    id = PrimaryKeyField(null=False)
    task = ForeignKeyField(Task, backref='notifications', null=True)
    user = ForeignKeyField(User, backref='notifications', null=True)
    title = CharField()
    relative_start_time = IntegerField()
    status = IntegerField(default=NotificationStatus.CREATED.value)


class UsersReadTasks(BaseModel):
    """
    UsersReadTasks model. If there is an entry with user and task it means that user can read this task
    """

    user = ForeignKeyField(User)
    task = ForeignKeyField(Task)


class UsersWriteTasks(BaseModel):
    """
    UsersWriteTasks model. If there is an entry with user and task it means that user can read and change this task
    """

    user = ForeignKeyField(User)
    task = ForeignKeyField(Task)


db.connect()
db.create_tables([User, Level, Task, UsersReadTasks,
                  UsersWriteTasks, Category, Notification, TaskPlan])
