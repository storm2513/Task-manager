import unittest
from peewee import *
from storage.storage_models import User, Level, Task, UsersReadTasks, UsersWriteTasks, Category
from storage.category_storage import CategoryStorage
from storage.level_storage import LevelStorage
from storage.task_storage import TaskStorage
from storage.user_storage import UserStorage
from models.task import Task as TaskInstance
from models.level import Level as LevelInstance
from models.user import User as UserInstance
from models.category import Category as CategoryInstance
from controllers.categories_controller import CategoriesController
from controllers.levels_controller import LevelsController
from controllers.tasks_controller import TasksController
from controllers.users_controller import UsersController
from tests.factories import *
from enums.status import Status

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

MODELS = [User, Level, Task, UsersReadTasks, UsersWriteTasks, Category]

categories_controller = CategoriesController(CategoryStorage())
levels_controller = LevelsController(LevelStorage())
users_controller = UsersController(UserStorage())
tasks_controller = TasksController(TaskStorage())
category = CategoryFactory()
user = UserFactory()
task = TaskFactory()


class ControllersTest(unittest.TestCase):
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

    # LevelsController tests

    def test_creates_level(self):
        before_levels_count = Level.select().count()
        levels_controller.create()
        after_levels_count = Level.select().count()
        self.assertEqual(before_levels_count + 1, after_levels_count)

    def test_increases_experience(self):
        level = levels_controller.create()
        old_experience = level.experience
        levels_controller.increase_experience(level)
        new_level = Level.get(Level.id == level.id)
        self.assertGreater(new_level.experience, old_experience)

    def test_deletes_level(self):
        level = levels_controller.create()
        levels_controller.delete(level.id)
        self.assertEqual(Level.select().where(Level.id == level.id).count(), 0)

    def test_gets_level_by_user_id(self):
        user_with_id = users_controller.create(user)
        level = LevelStorage().get_by_id(user_with_id.level_id)
        level_from_test_method = levels_controller.get_by_user_id(
            user_with_id.id)
        self.assertEqual(level.id, level_from_test_method.id)
        self.assertEqual(level.experience, level_from_test_method.experience)

    # UsersController tests

    def test_creates_user(self):
        before_users_count = User.select().count()
        users_controller.create(user)
        after_users_count = User.select().count()
        self.assertEqual(before_users_count + 1, after_users_count)

    def test_gets_user_by_id(self):
        user_with_id = users_controller.create(user)
        user_from_test_method = users_controller.get_by_id(user_with_id.id)
        self.assertEqual(user_with_id.id, user_from_test_method.id)
        self.assertEqual(user_with_id.name, user_from_test_method.name)
        self.assertEqual(user_with_id.email, user_from_test_method.email)
        self.assertEqual(user_with_id.password, user_from_test_method.password)

    def test_gets_user_by_email(self):
        user.email = "example@mail.com"
        users_controller.create(user)
        user_from_test_method = users_controller.get_by_email(user.email)
        self.assertEqual(user.email, user_from_test_method.email)

    def test_updates_user(self):
        user_with_id = users_controller.create(user)
        user_with_id.name = "Maksim"
        users_controller.update(user_with_id)
        user_from_test_method = users_controller.get_by_id(user_with_id.id)
        self.assertEqual(user_with_id.name, user_from_test_method.name)

    def test_deletes_user(self):
        user_with_id = users_controller.create(user)
        users_controller.delete(user_with_id.id)
        self.assertEqual(users_controller.get_by_id(user_with_id.id), None)

    # CategoriesController tests

    def test_creates_category(self):
        before_categories_count = Category.select().count()
        user_id = users_controller.create(user).id
        categories_controller.create(category, user_id)
        after_categories_count = Category.select().count()
        self.assertEqual(before_categories_count + 1, after_categories_count)

    def gets_category_by_id(self):
        user_id = users_controller.create(user).id
        category_with_id = categories_controller.create(category, user_id)
        category_from_test_method = categories_controller.get_by_id(
            category_id)
        self.assertEqual(category_with_id.id, category_from_test_method.id)
        self.assertEqual(category_with_id.name, category_from_test_method.name)
        self.assertEqual(
            category_with_id.user_id,
            category_from_test_method.user_id)

    def test_updates_category(self):
        user_id = users_controller.create(user).id
        category_with_id = categories_controller.create(category, user_id)
        category_with_id.name = "Movies to watch"
        categories_controller.update(category_with_id)
        category_from_test_method = categories_controller.get_by_id(
            category_with_id.id)
        self.assertEqual(category_with_id.name, category_from_test_method.name)

    def test_deletes_category(self):
        user_id = users_controller.create(user).id
        category_with_id = categories_controller.create(category, user_id)
        categories_controller.delete(category_with_id.id)
        self.assertEqual(
            categories_controller.get_by_id(
                category_with_id.id), None)

    # TasksController tests

    def test_creates_task(self):
        before_tasks_count = Task.select().count()
        tasks_controller.create(task)
        after_tasks_count = Task.select().count()
        self.assertEqual(before_tasks_count + 1, after_tasks_count)

    def test_gets_task_by_id(self):
        task_with_id = tasks_controller.create(task)
        task_from_test_method = tasks_controller.get_by_id(task_with_id.id)
        self.assertEqual(task_with_id.id, task_from_test_method.id)

    def test_deletes_task(self):
        task_with_id = tasks_controller.create(task)
        tasks_controller.delete(task_with_id.id)
        self.assertEqual(tasks_controller.get_by_id(task_with_id.id), None)

    def test_updates_task(self):
        task_with_id = tasks_controller.create(task)
        task_with_id.title = "More movies to watch"
        tasks_controller.update(task_with_id)
        task_from_test_method = tasks_controller.get_by_id(task_with_id.id)
        self.assertEqual(task_with_id.title, task_from_test_method.title)

    def test_sets_task_as_todo(self):
        task.status = Status.IN_PROGRESS.value
        task_id = tasks_controller.create(task).id
        tasks_controller.set_as_to_do(task_id)
        task_from_test_method = tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.TODO.value)

    def test_sets_task_as_in_progress(self):
        task.status = Status.TODO.value
        task_id = tasks_controller.create(task).id
        tasks_controller.set_as_in_progress(task_id)
        task_from_test_method = tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.IN_PROGRESS.value)

    def test_sets_task_as_done(self):
        user_with_id = users_controller.create(user)
        task.user_id = user_with_id.id
        task.status = Status.TODO.value
        task_id = tasks_controller.create(task).id
        tasks_controller.set_as_done(task_id)
        task_from_test_method = tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.DONE.value)

    def test_sets_task_as_archive(self):
        task.status = Status.TODO.value
        task_id = tasks_controller.create(task).id
        tasks_controller.set_as_archived(task_id)
        task_from_test_method = tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.ARCHIVED.value)

    def test_returns_user_tasks(self):
        user_id = users_controller.create(user).id
        task.user_id = user_id
        first_task = tasks_controller.create(task)
        second_task = tasks_controller.create(task)
        tasks = tasks_controller.user_tasks(user_id)
        self.assertEqual(len(tasks), 2)

    def test_creates_inner_task(self):
        task_id = tasks_controller.create(task).id
        inner_task = tasks_controller.create_inner_task(task_id, task)
        self.assertEqual(inner_task.parent_task_id, task_id)

    def test_returns_inner_tasks(self):
        task.parent_task_id = None
        task_id = tasks_controller.create(task).id
        tasks_controller.create_inner_task(task_id, task)
        tasks_controller.create_inner_task(task_id, task)
        inner_tasks = tasks_controller.inner(task_id)
        self.assertEqual(len(inner_tasks), 2)

    def test_assignes_task_on_user(self):
        user_id = users_controller.create(user).id
        task_id = tasks_controller.create(task).id
        tasks_controller.assign_task_on_user(task_id, user_id)
        self.assertEqual(
            Task.select().where(
                Task.assigned_user_id == user_id).count(), 1)

    def test_adds_user_for_read(self):
        user_id = users_controller.create(user).id
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            1)

    def test_adds_user_for_write(self):
        user_id = users_controller.create(user).id
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_write(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            1)

    def test_removes_user_for_read(self):
        user_id = users_controller.create(user).id
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_read(user_id=user_id, task_id=task_id)
        tasks_controller.remove_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            0)

    def test_removes_user_for_write(self):
        user_id = users_controller.create(user).id
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_write(user_id=user_id, task_id=task_id)
        tasks_controller.remove_user_for_write(
            user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            0)
