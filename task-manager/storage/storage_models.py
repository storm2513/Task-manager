from peewee import *
import datetime

from enums.status import Status
from enums.priority import Priority

db = SqliteDatabase('task_manager.db')


class BaseModel(Model):
    class Meta:
        database = db


class Level(BaseModel):
    id = PrimaryKeyField(null=False)
    experience = IntegerField(default=1)


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    email = CharField()
    name = CharField()
    password = CharField()
    level = ForeignKeyField(Level, backref='user')


class Category(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()
    user = ForeignKeyField(User, backref='categories')


class Task(BaseModel):
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
    priority = IntegerField(default=Priority.MEDIUM)
    status = IntegerField(default=Status.TODO)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Task, self).save(*args, **kwargs)

    def assign_user(self, user):
        self.assigned_user = user
        self.save()

    def parent(self):
        return Task.get(Task.id == self.parent_task_id)

    def inner(self):
        return list(Task.select().where(Task.parent_task_id == self.id))

    def create_inner(self, **params):
        task = Task.create(**params)
        task.parent_task_id = self.id
        task.user = self.user
        task.save()

    def add_user_for_read(self, user):
        if UsersReadTasks.select().where(
                UsersReadTasks.task == self and UsersReadTasks.user == user).count() == 0:
            UsersReadTasks.create(task=self, user=user)

    def add_user_for_write(self, user):
        if UsersWriteTasks.select().where(
                UsersWriteTasks.task == self and UsersWriteTasks.user == user).count() == 0:
            UsersWriteTasks.create(task=self, user=user)

    def remove_user_for_read(self, user):
        query = UsersReadTasks.delete().where(
            UsersReadTasks.task == self and UsersReadTasks.user == user)
        query.execute()

    def remove_user_for_write(self, user):
        query = UsersWriteTasks.delete().where(
            UsersWriteTasks.task == self and UsersWriteTasks.user == user)
        query.execute()


class UsersReadTasks(BaseModel):
    user = ForeignKeyField(User)
    task = ForeignKeyField(Task)


class UsersWriteTasks(BaseModel):
    user = ForeignKeyField(User)
    task = ForeignKeyField(Task)


db.connect()
db.create_tables([User, Level, Task, UsersReadTasks,
                  UsersWriteTasks, Category])
