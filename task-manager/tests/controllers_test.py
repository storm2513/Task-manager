import datetime
import unittest
from lib.storage.storage_models import Task, TaskPlan, UsersReadTasks, UsersWriteTasks, Category, Adapter, Notification
from lib.storage.category_storage import CategoryStorage
from lib.storage.notification_storage import NotificationStorage
from lib.storage.task_storage import TaskStorage
from lib.storage.task_plan_storage import TaskPlanStorage
from lib.models.notification import Status as NotificationStatus
from lib.models.task import Status
from lib.controllers.categories_controller import CategoriesController
from lib.controllers.notifications_controller import NotificationsController
from lib.controllers.tasks_controller import TasksController
from lib.controllers.task_plans_controller import TaskPlansController
from tests.factories import CategoryFactory, TaskFactory, TaskPlanFactory, NotificationFactory

# use an in-memory SQLite for tests.
database = ':memory:'

user_id = 10
categories_controller = CategoriesController(
    user_id, CategoryStorage(database))
tasks_controller = TasksController(user_id, TaskStorage(database))
task_plans_controller = TaskPlansController(user_id, TaskPlanStorage(database))
notifications_controller = NotificationsController(
    user_id, NotificationStorage(database))
category = CategoryFactory()
task = TaskFactory()
task_plan = TaskPlanFactory()
notification = NotificationFactory()


class ControllersTest(unittest.TestCase):
    def setUp(self):
        Adapter(database).create_tables()

    def tearDown(self):
        Adapter(database).drop_tables()

    # CategoriesController tests

    def test_creates_category(self):
        before_categories_count = Category.select().count()
        categories_controller.create(category)
        after_categories_count = Category.select().count()
        self.assertEqual(before_categories_count + 1, after_categories_count)

    def gets_category_by_id(self):
        category_with_id = categories_controller.create(category)
        category_from_test_method = categories_controller.get_by_id(
            category_id)
        self.assertEqual(category_with_id.id, category_from_test_method.id)
        self.assertEqual(category_with_id.name, category_from_test_method.name)
        self.assertEqual(
            category_with_id.user_id,
            category_from_test_method.user_id)

    def test_updates_category(self):
        category_with_id = categories_controller.create(category)
        category_with_id.name = "Movies to watch"
        categories_controller.update(category_with_id)
        category_from_test_method = categories_controller.get_by_id(
            category_with_id.id)
        self.assertEqual(category_with_id.name, category_from_test_method.name)

    def test_deletes_category(self):
        category_with_id = categories_controller.create(category)
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
        self.assertEqual(
            task_from_test_method.status,
            Status.IN_PROGRESS.value)

    def test_sets_task_as_done(self):
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
        first_task = tasks_controller.create(task)
        second_task = tasks_controller.create(task)
        tasks = tasks_controller.user_tasks()
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
        user_id = 5
        task_id = tasks_controller.create(task).id
        tasks_controller.assign_task_on_user(task_id, user_id)
        self.assertEqual(
            Task.select().where(
                Task.assigned_user_id == user_id).count(), 1)

    def test_adds_user_for_read(self):
        user_id = 5
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            1)

    def test_adds_user_for_write(self):
        user_id = 5
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_write(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            1)

    def test_removes_user_for_read(self):
        user_id = 5
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_read(user_id=user_id, task_id=task_id)
        tasks_controller.remove_user_for_read(user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            0)

    def test_removes_user_for_write(self):
        user_id = 5
        task_id = tasks_controller.create(task).id
        tasks_controller.add_user_for_write(user_id=user_id, task_id=task_id)
        tasks_controller.remove_user_for_write(
            user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            0)

    # TaskPlansController tests

    def test_creates_task_plan(self):
        before_plans_count = TaskPlan.select().count()
        task_plans_controller.create(task_plan)
        after_plans_count = TaskPlan.select().count()
        self.assertEqual(before_plans_count + 1, after_plans_count)

    def test_deletes_task_plan_by_id(self):
        task_plan_id = task_plans_controller.create(task_plan).id
        task_plans_controller.delete(task_plan_id)
        self.assertEqual(TaskPlan.select().where(
            TaskPlan.id == task_plan_id).count(), 0)

    def test_updates_task_plan(self):
        new_interval = 500
        new_datetime = datetime.datetime.now()
        task_plan_with_id = task_plans_controller.create(task_plan)
        task_plan_with_id.interval = new_interval
        task_plan_with_id.last_created_at = new_datetime
        task_plans_controller.update(task_plan_with_id)
        task_plan_from_db = TaskPlan.get(TaskPlan.id == task_plan_with_id.id)
        self.assertEqual(task_plan_from_db.interval, new_interval)
        self.assertEqual(task_plan_from_db.last_created_at, new_datetime)

    def test_returns_all_user_plans(self):
        user_id = 10
        task_plan.user_id = 10
        plans_count = 3
        for i in range(plans_count):
            task_plans_controller.create(task_plan)
        plans = task_plans_controller.all()
        self.assertEqual(len(plans), plans_count)

    def test_processes_task_plans(self):
        user_id = 10
        repeated_task = TaskFactory()
        repeated_task.status = Status.TEMPLATE.value
        repeated_task.user_id = user_id
        task_id = tasks_controller.create(repeated_task).id
        before_tasks_count = len(tasks_controller.user_tasks())
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
        task_plans_controller.create(repeated_task_plan)
        task_plans_controller.create(repeated_task_plan_big_interval)
        task_plans_controller.process_plans(tasks_controller)
        self.assertEqual(len(tasks_controller.user_tasks()),
                         before_tasks_count + 1)

    # NotificationsController tests

    def test_creates_notification(self):
        before_notifications_count = Notification.select().count()
        notifications_controller.create(notification)
        after_notifications_count = Notification.select().count()
        self.assertEqual(
            before_notifications_count + 1,
            after_notifications_count)

    def test_deletes_notification_by_id(self):
        notification_id = notifications_controller.create(notification).id
        notifications_controller.delete(notification_id)
        self.assertEqual(Notification.select().where(
            Notification.id == notification_id).count(), 0)

    def test_updates_notification(self):
        new_title = "Updated title"
        notification_with_id = notifications_controller.create(notification)
        notification_with_id.title = new_title
        notifications_controller.update(notification_with_id)
        notification_from_db = Notification.get(
            Notification.id == notification_with_id.id)
        self.assertEqual(notification_from_db.title, new_title)

    def test_returns_all_user_notifications(self):
        user_id = 10
        notification.user_id = 10
        notifications_count = 3
        for i in range(notifications_count):
            notifications_controller.create(notification)
        notifications = notifications_controller.all()
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_pending_notifications(self):
        user_id = 10
        notification.user_id = 10
        notification.status = NotificationStatus.PENDING.value
        notifications_count = 3
        for i in range(notifications_count):
            notifications_controller.create(notification)
        # create notification with other status
        notification.status = NotificationStatus.CREATED.value
        notifications_controller.create(notification)
        notifications = notifications_controller.pending()
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_created_notifications(self):
        user_id = 10
        notification.user_id = 10
        notification.status = NotificationStatus.CREATED.value
        notifications_count = 3
        for i in range(notifications_count):
            notifications_controller.create(notification)
        # create notification with other status
        notification.status = NotificationStatus.PENDING.value
        notifications_controller.create(notification)
        notifications = notifications_controller.created()
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_pending_notifications(self):
        user_id = 10
        notification.user_id = 10
        notification.status = NotificationStatus.SHOWN.value
        notifications_count = 3
        for i in range(notifications_count):
            notifications_controller.create(notification)
        # create notification with other status
        notification.status = NotificationStatus.CREATED.value
        notifications_controller.create(notification)
        notifications = notifications_controller.shown()
        self.assertEqual(len(notifications), notifications_count)

    def test_process_notification(self):
        task.start_time = datetime.datetime.now()
        task_id = tasks_controller.create(task).id
        relative_start_time = 300
        notification.status = NotificationStatus.CREATED.value
        notification.relative_start_time = 300
        notification.task_id = task_id
        notification_id = notifications_controller.create(notification).id
        notifications_controller.process_notifications()
        processed_notification = notifications_controller.get_by_id(
            notification_id)
        self.assertEqual(
            processed_notification.status,
            NotificationStatus.PENDING.value)

    def test_sets_notification_status_as_shown(self):
        notification_with_id = notifications_controller.create(notification)
        notifications_controller.set_as_shown(notification_with_id.id)
        notification_from_db = Notification.get(
            Notification.id == notification_with_id.id)
        self.assertEqual(
            notification_from_db.status,
            NotificationStatus.SHOWN.value)
