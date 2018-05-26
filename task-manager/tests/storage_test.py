import unittest
from peewee import *
from storage.storage_models import User, Level, Task, UsersReadTasks, UsersWriteTasks, Category, TaskPlan
from storage.category_storage import CategoryStorage
from storage.level_storage import LevelStorage
from storage.task_storage import TaskStorage
from storage.user_storage import UserStorage
from storage.task_plan_storage import TaskPlanStorage
from models.task import Task as TaskInstance
from models.level import Level as LevelInstance
from models.user import User as UserInstance
from models.category import Category as CategoryInstance
from models.task_plan import TaskPlan as TaskPlanInstance
from tests.factories import *

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

MODELS = [User, Level, Task, UsersReadTasks, UsersWriteTasks, Category]

level_storage = LevelStorage()
user_storage = UserStorage()
category_storage = CategoryStorage()
task_storage = TaskStorage()
task_plan_storage = TaskPlanStorage()
user = UserFactory()
category = CategoryFactory(user_id=10)
task = TaskFactory()
task_plan = TaskPlanFactory()


class StorageTest(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db
        for model in MODELS:
            model.bind(test_db, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        # Close connection to db.
        test_db.close()

    # LevelStorage tests

    def test_creates_level(self):
        before_levels_count = Level.select().count()
        level_storage.create()
        after_levels_count = Level.select().count()
        self.assertEqual(before_levels_count + 1, after_levels_count)

    def test_creates_level_and_gets_it_by_id(self):
        level = level_storage.create()
        level_from_db = level_storage.get_by_id(level.id)
        self.assertEqual(level.id, level_from_db.id)
        self.assertEqual(level.experience, level_from_db.experience)

    def test_creates_level_and_gets_it_by_user_id(self):
        level = level_storage.create()
        user.level_id = level.id
        user_id = user_storage.create(user).id
        level_from_db = level_storage.get_by_user_id(user_id)
        self.assertEqual(level.id, level_from_db.id)
        self.assertEqual(level.experience, level_from_db.experience)

    def test_deletes_level_by_id(self):
        level_id = level_storage.create().id
        level_storage.delete_by_id(level_id)
        self.assertEqual(Level.select().where(Level.id == level_id).count(), 0)

    def test_updates_level(self):
        level = level_storage.create()
        level.experience = 10
        level_storage.update(level)
        experience = Level.get(Level.id == level.id).experience
        self.assertEqual(experience, 10)

    # UserStorage tests

    def test_creates_user(self):
        before_users_count = User.select().count()
        user_storage.create(user)
        after_users_count = User.select().count()
        self.assertEqual(before_users_count + 1, after_users_count)

    def test_creates_user_and_gets_id_by_id(self):
        user_with_id = user_storage.create(user)
        user_from_db = user_storage.get_by_id(user_with_id.id)
        self.assertEqual(user_with_id.id, user_from_db.id)
        self.assertEqual(user_with_id.email, user_from_db.email)
        self.assertEqual(user_with_id.name, user_from_db.name)
        self.assertEqual(user_with_id.password, user_from_db.password)

    def test_creates_user_and_gets_id_by_email(self):
        user_with_id = user_storage.create(user)
        user_from_db = user_storage.get_by_email(user_with_id.email)
        self.assertEqual(user_with_id.id, user_from_db.id)
        self.assertEqual(user_with_id.email, user_from_db.email)
        self.assertEqual(user_with_id.name, user_from_db.name)
        self.assertEqual(user_with_id.password, user_from_db.password)

    def test_deletes_user_by_id(self):
        user_id = user_storage.create(user).id
        user_storage.delete_by_id(user_id)
        self.assertEqual(User.select().where(User.id == user_id).count(), 0)

    def test_updates_user(self):
        user_with_id = user_storage.create(user)
        user_with_id.name = "Maksim"
        user_with_id.password = "12345678"
        user_storage.update(user_with_id)
        user_from_db = User.get(User.id == user_with_id.id)
        self.assertEqual(user_from_db.name, "Maksim")
        self.assertEqual(user_from_db.password, "12345678")

    # CategoryStorage tests

    def test_creates_category(self):
        before_categories_count = Category.select().count()
        category_storage.create(category)
        after_categories_count = Category.select().count()
        self.assertEqual(before_categories_count + 1, after_categories_count)

    def test_creates_category_and_gets_it_by_id(self):
        category_with_id = category_storage.create(category)
        category_from_db = category_storage.get_by_id(category_with_id.id)
        self.assertEqual(category_with_id.id, category_from_db.id)
        self.assertEqual(category_with_id.name, category_from_db.name)
        self.assertEqual(category_with_id.user_id, category_from_db.user_id)

    def test_deletes_category_by_id(self):
        category_id = category_storage.create(category).id
        category_storage.delete_by_id(category_id)
        self.assertEqual(
            Category.select().where(
                Category.id == category_id).count(), 0)

    def test_updates_category(self):
        category_with_id = category_storage.create(category)
        category_with_id.name = "Movies to watch"
        category_storage.update(category_with_id)
        category_from_db = Category.get(Category.id == category_with_id.id)
        self.assertEqual(category_from_db.name, "Movies to watch")

    # TaskStorage tests

    def test_creates_task(self):
        before_tasks_count = Task.select().count()
        task_storage.create(task)
        after_tasks_count = Task.select().count()
        self.assertEqual(before_tasks_count + 1, after_tasks_count)

    def test_creates_task_and_gets_it_by_id(self):
        task_with_id = task_storage.create(task)
        task_from_db = task_storage.get_by_id(task_with_id.id)
        self.assertEqual(task_with_id.id, task_from_db.id)
        self.assertEqual(task_with_id.title, task_from_db.title)
        self.assertEqual(task_with_id.user_id, task_from_db.user_id)
        self.assertEqual(task_with_id.note, task_from_db.note)

    def test_deletes_task_by_id(self):
        task_id = task_storage.create(task).id
        task_storage.delete_by_id(task_id)
        self.assertEqual(Task.select().where(Task.id == task_id).count(), 0)

    def test_updates_task(self):
        task_with_id = task_storage.create(task)
        task_with_id.title = "Do something great"
        task_storage.update(task_with_id)
        task_from_db = Task.get(Task.id == task_with_id.id)
        self.assertEqual(task_from_db.title, "Do something great")

    def test_returns_user_tasks(self):
        first_task = TaskFactory()
        second_task = TaskFactory()
        user_id = user_storage.create(user).id
        first_task.user_id = user_id
        second_task.user_id = user_id
        task_storage.create(first_task)
        task_storage.create(second_task)
        tasks = task_storage.user_tasks(user_id)
        self.assertEqual(len(tasks), 2)

    def test_returns_inner_tasks(self):
        task_id = task_storage.create(task).id
        inner_task = TaskFactory()
        inner_task.parent_task_id = task_id
        task_storage.create(inner_task)
        inner_tasks = task_storage.inner(task_id)
        self.assertEqual(len(inner_tasks), 1)

    def test_adds_user_for_read(self):
        user_id = user_storage.create(user).id
        task_id = task_storage.create(task).id
        task_storage.add_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            1)

    def test_adds_user_for_write(self):
        user_id = user_storage.create(user).id
        task_id = task_storage.create(task).id
        task_storage.add_user_for_write(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            1)

    def test_removes_user_for_read(self):
        user_id = user_storage.create(user).id
        task_id = task_storage.create(task).id
        task_storage.add_user_for_read(user_id=user_id, task_id=task_id)
        task_storage.remove_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            0)

    def test_removes_user_for_write(self):
        user_id = user_storage.create(user).id
        task_id = task_storage.create(task).id
        task_storage.add_user_for_write(user_id=user_id, task_id=task_id)
        task_storage.remove_user_for_write(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            0)

    # TaskPlanStorage tests

    def test_creates_task_plan(self):
        before_plans_count = TaskPlan.select().count()
        task_plan_storage.create(task_plan)
        after_plans_count = TaskPlan.select().count()
        self.assertEqual(before_plans_count + 1, after_plans_count)

    def test_deletes_task_plan_by_id(self):
        task_plan_id = task_plan_storage.create(task_plan).id
        task_plan_storage.delete_by_id(task_plan_id)
        self.assertEqual(TaskPlan.select().where(TaskPlan.id == task_plan_id).count(), 0)
