from peewee import (
    Proxy,
    Model,
    PrimaryKeyField,
    IntegerField,
    CharField,
    ForeignKeyField,
    DateTimeField,
    BooleanField,
    SqliteDatabase)
import datetime
from tmlib.models.task import Status, Priority
from tmlib.models.notification import Status as NotificationStatus

database_proxy = Proxy()


class BaseModel(Model):
    """
    Base class for classes that work with peewee library
    """

    class Meta:
        database = database_proxy


class Category(BaseModel):
    """
    Category model
    """

    id = PrimaryKeyField(null=False)
    name = CharField()
    user_id = IntegerField(null=True)


class Task(BaseModel):
    """
    Task model
    """

    id = PrimaryKeyField(null=False)
    user_id = IntegerField(null=True)
    title = CharField()
    note = CharField(default="")
    start_time = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    assigned_user_id = IntegerField(null=True)
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
    user_id = IntegerField(null=True)
    task = ForeignKeyField(Task, null=True)
    interval = IntegerField()
    last_created_at = DateTimeField()


class Notification(BaseModel):
    """
    Notification model
    """

    id = PrimaryKeyField(null=False)
    task = ForeignKeyField(Task, backref='notifications', null=True)
    user_id = IntegerField(null=True)
    title = CharField()
    relative_start_time = IntegerField()
    status = IntegerField(default=NotificationStatus.CREATED.value)


class UsersReadTasks(BaseModel):
    """
    UsersReadTasks model. If there is an entry with user and task it means that user can read this task
    """

    user_id = IntegerField(null=True)
    task = ForeignKeyField(Task)


class UsersWriteTasks(BaseModel):
    """
    UsersWriteTasks model. If there is an entry with user and task it means that user can read and change this task
    """

    user_id = IntegerField(null=True)
    task = ForeignKeyField(Task)


class Adapter:
    def __init__(self, database_name='task-manager.db'):
        self.database_name = database_name
        self.database = SqliteDatabase(database_name)
        self.connected = False
        database_proxy.initialize(self.database)
        self.create_tables()

    def create_tables(self):
        if not self.connected:
            self.database.connect()
            self.connected = True
        Category.create_table(True)
        Notification.create_table(True)
        Task.create_table(True)
        TaskPlan.create_table(True)
        UsersReadTasks.create_table(True)
        UsersWriteTasks.create_table(True)

    def drop_tables(self):
        self.database.drop_tables(
            [Task, UsersReadTasks, UsersWriteTasks, Category, Notification, TaskPlan])
        self.database.close()
        self.connected = False
