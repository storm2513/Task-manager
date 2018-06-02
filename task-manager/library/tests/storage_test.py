import unittest
import datetime
from tmlib.storage.storage_models import Task, UsersReadTasks, UsersWriteTasks, Category, TaskPlan, Notification, Adapter
from tmlib.storage.category_storage import CategoryStorage
from tmlib.storage.notification_storage import NotificationStorage
from tmlib.storage.task_storage import TaskStorage
from tmlib.storage.task_plan_storage import TaskPlanStorage
from tmlib.models.task import Status
from tmlib.models.notification import Status as NotificationStatus
from tests.factories import CategoryFactory, TaskFactory, TaskPlanFactory, NotificationFactory

# use an in-memory SQLite for tests.
database = ':memory:'

category_storage = CategoryStorage(database)
task_storage = TaskStorage(database)
task_plan_storage = TaskPlanStorage(database)
notification_storage = NotificationStorage(database)
category = CategoryFactory(user_id=10)
task = TaskFactory()
task_plan = TaskPlanFactory()
notification = NotificationFactory()


class StorageTest(unittest.TestCase):
    def setUp(self):
        Adapter(database).create_tables()

    def tearDown(self):
        Adapter(database).drop_tables()

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
        user_id = 10
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
        user_id = 10
        task_id = task_storage.create(task).id
        task_storage.add_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            1)

    def test_adds_user_for_write(self):
        user_id = 10
        task_id = task_storage.create(task).id
        task_storage.add_user_for_write(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            1)

    def test_removes_user_for_read(self):
        user_id = 10
        task_id = task_storage.create(task).id
        task_storage.add_user_for_read(user_id=user_id, task_id=task_id)
        task_storage.remove_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            0)

    def test_removes_user_for_write(self):
        user_id = 10
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
        self.assertEqual(TaskPlan.select().where(
            TaskPlan.id == task_plan_id).count(), 0)

    def test_updates_task_plan(self):
        new_interval = 500
        new_datetime = datetime.datetime.now()
        task_plan_with_id = task_plan_storage.create(task_plan)
        task_plan_with_id.interval = new_interval
        task_plan_with_id.last_created_at = new_datetime
        task_plan_storage.update(task_plan_with_id)
        task_plan_from_db = TaskPlan.get(TaskPlan.id == task_plan_with_id.id)
        self.assertEqual(task_plan_from_db.interval, new_interval)
        self.assertEqual(task_plan_from_db.last_created_at, new_datetime)

    def test_returns_all_user_plans(self):
        user_id = 10
        task_plan.user_id = 10
        plans_count = 3
        for i in range(plans_count):
            task_plan_storage.create(task_plan)
        plans = task_plan_storage.all_user_plans(user_id)
        self.assertEqual(len(plans), plans_count)

    def test_processes_task_plans(self):
        user_id = 10
        repeated_task = TaskFactory()
        repeated_task.status = Status.TEMPLATE.value
        repeated_task.user_id = user_id
        task_id = task_storage.create(repeated_task).id
        before_tasks_count = len(task_storage.user_tasks(user_id))
        interval = 300
        big_interval = interval * 10
        last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval + 5)
        """
        repeated_task_plan after processing should create new task
        repeated_task_plan_big_interval should not create new task because of bit interval
        """
        repeated_task_plan = TaskPlan(
            user_id=user_id,
            task_id=task_id,
            last_created_at=last_created_at,
            interval=interval)
        repeated_task_plan_big_interval = TaskPlan(
            user_id=user_id,
            task_id=task_id,
            last_created_at=last_created_at,
            interval=big_interval)
        task_plan_storage.create(repeated_task_plan)
        task_plan_storage.create(repeated_task_plan_big_interval)
        task_plan_storage.process_plans(task_storage)
        self.assertEqual(len(task_storage.user_tasks(user_id)),
                         before_tasks_count + 1)

    # NotificationStorage tests

    def test_creates_notification(self):
        before_notifications_count = Notification.select().count()
        notification_storage.create(notification)
        after_notifications_count = Notification.select().count()
        self.assertEqual(
            before_notifications_count + 1,
            after_notifications_count)

    def test_deletes_notification_by_id(self):
        notification_id = notification_storage.create(notification).id
        notification_storage.delete_by_id(notification_id)
        self.assertEqual(Notification.select().where(
            Notification.id == notification_id).count(), 0)

    def test_updates_notification(self):
        new_title = "Updated title"
        notification_with_id = notification_storage.create(notification)
        notification_with_id.title = new_title
        notification_storage.update(notification_with_id)
        notification_from_db = Notification.get(
            Notification.id == notification_with_id.id)
        self.assertEqual(notification_from_db.title, new_title)

    def test_returns_all_user_notifications(self):
        user_id = 10
        notification.user_id = 10
        notifications_count = 3
        for i in range(notifications_count):
            notification_storage.create(notification)
        notifications = notification_storage.all_user_notifications(user_id)
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_pending_notifications(self):
        user_id = 10
        notification.user_id = 10
        notification.status = NotificationStatus.PENDING.value
        notifications_count = 3
        for i in range(notifications_count):
            notification_storage.create(notification)
        # create notification with other status
        notification.status = NotificationStatus.CREATED.value
        notification_storage.create(notification)
        notifications = notification_storage.pending(user_id)
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_created_notifications(self):
        user_id = 10
        notification.user_id = 10
        notification.status = NotificationStatus.CREATED.value
        notifications_count = 3
        for i in range(notifications_count):
            notification_storage.create(notification)
        # create notification with other status
        notification.status = NotificationStatus.PENDING.value
        notification_storage.create(notification)
        notifications = notification_storage.created(user_id)
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_pending_notifications(self):
        user_id = 10
        notification.user_id = 10
        notification.status = NotificationStatus.SHOWN.value
        notifications_count = 3
        for i in range(notifications_count):
            notification_storage.create(notification)
        # create notification with other status
        notification.status = NotificationStatus.CREATED.value
        notification_storage.create(notification)
        notifications = notification_storage.shown(user_id)
        self.assertEqual(len(notifications), notifications_count)

    def test_process_notification(self):
        task.start_time = datetime.datetime.now()
        task_id = task_storage.create(task).id
        relative_start_time = 300
        notification.status = NotificationStatus.CREATED.value
        notification.relative_start_time = 300
        notification.task_id = task_id
        notification_id = notification_storage.create(notification).id
        notification_storage.process_notifications()
        processed_notification = notification_storage.get_by_id(
            notification_id)
        self.assertEqual(
            processed_notification.status,
            NotificationStatus.PENDING.value)
