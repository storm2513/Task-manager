import datetime
import unittest
from tmlib.storage.storage_models import (
    Task,
    TaskPlan,
    UsersReadTasks,
    UsersWriteTasks,
    Category,
    DatabaseConnector,
    Notification)
from tmlib.storage.category_storage import CategoryStorage
from tmlib.storage.notification_storage import NotificationStorage
from tmlib.storage.task_storage import TaskStorage
from tmlib.storage.task_plan_storage import TaskPlanStorage
from tmlib.models.notification import Status as NotificationStatus
from tmlib.models.task import Status
from tmlib.controllers.categories_controller import CategoriesController
from tmlib.controllers.notifications_controller import NotificationsController
from tmlib.controllers.tasks_controller import TasksController
from tmlib.controllers.task_plans_controller import TaskPlansController
from tests.factories import CategoryFactory, TaskFactory, TaskPlanFactory, NotificationFactory


class ControllersTest(unittest.TestCase):
    def setUp(self):
        self.database = ':memory:'

        self.user_id = 10
        self.categories_controller = CategoriesController(
            self.user_id, CategoryStorage(self.database))
        self.tasks_controller = TasksController(
            self.user_id, TaskStorage(self.database))
        self.task_plans_controller = TaskPlansController(
            self.user_id, TaskPlanStorage(self.database))
        self.notifications_controller = NotificationsController(
            self.user_id, NotificationStorage(self.database))
        self.category = CategoryFactory()
        self.task = TaskFactory()
        self.task_plan = TaskPlanFactory()
        self.notification = NotificationFactory()
        DatabaseConnector(self.database).create_tables()

    def tearDown(self):
        DatabaseConnector(self.database).drop_tables()

    # CategoriesController tests

    def test_creates_category(self):
        before_categories_count = Category.select().count()
        self.categories_controller.create(self.category)
        after_categories_count = Category.select().count()
        self.assertEqual(before_categories_count + 1, after_categories_count)

    def gets_category_by_id(self):
        category_with_id = self.categories_controller.create(self.category)
        category_from_test_method = self.categories_controller.get_by_id(
            category_id)
        self.assertEqual(category_with_id.id, category_from_test_method.id)
        self.assertEqual(category_with_id.name, category_from_test_method.name)
        self.assertEqual(
            category_with_id.user_id,
            category_from_test_method.user_id)

    def test_updates_category(self):
        category_with_id = self.categories_controller.create(self.category)
        category_with_id.name = "Movies to watch"
        self.categories_controller.update(category_with_id)
        category_from_test_method = self.categories_controller.get_by_id(
            category_with_id.id)
        self.assertEqual(category_with_id.name, category_from_test_method.name)

    def test_deletes_category(self):
        category_with_id = self.categories_controller.create(self.category)
        self.categories_controller.delete(category_with_id.id)
        self.assertEqual(
            self.categories_controller.get_by_id(
                category_with_id.id), None)

    # TasksController tests

    def test_creates_task(self):
        before_tasks_count = Task.select().count()
        self.tasks_controller.create(self.task)
        after_tasks_count = Task.select().count()
        self.assertEqual(before_tasks_count + 1, after_tasks_count)

    def test_gets_task_by_id(self):
        task_with_id = self.tasks_controller.create(self.task)
        task_from_test_method = self.tasks_controller.get_by_id(
            task_with_id.id)
        self.assertEqual(task_with_id.id, task_from_test_method.id)

    def test_deletes_task(self):
        task_with_id = self.tasks_controller.create(self.task)
        self.tasks_controller.delete(task_with_id.id)
        self.assertEqual(
            self.tasks_controller.get_by_id(
                task_with_id.id), None)

    def test_updates_task(self):
        task_with_id = self.tasks_controller.create(self.task)
        task_with_id.title = "More movies to watch"
        self.tasks_controller.update(task_with_id)
        task_from_test_method = self.tasks_controller.get_by_id(
            task_with_id.id)
        self.assertEqual(task_with_id.title, task_from_test_method.title)

    def test_sets_task_as_todo(self):
        self.task.status = Status.IN_PROGRESS.value
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.set_status(task_id, Status.TODO.value)
        task_from_test_method = self.tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.TODO.value)

    def test_sets_task_as_in_progress(self):
        self.task.status = Status.TODO.value
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.set_status(task_id, Status.IN_PROGRESS.value)
        task_from_test_method = self.tasks_controller.get_by_id(task_id)
        self.assertEqual(
            task_from_test_method.status,
            Status.IN_PROGRESS.value)

    def test_sets_task_as_done(self):
        self.task.status = Status.TODO.value
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.set_status(task_id, Status.DONE.value)
        task_from_test_method = self.tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.DONE.value)

    def test_sets_task_as_archive(self):
        self.task.status = Status.TODO.value
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.set_status(task_id, Status.ARCHIVED.value)
        task_from_test_method = self.tasks_controller.get_by_id(task_id)
        self.assertEqual(task_from_test_method.status, Status.ARCHIVED.value)

    def test_returns_user_tasks(self):
        first_task = self.tasks_controller.create(self.task)
        second_task = self.tasks_controller.create(self.task)
        tasks = self.tasks_controller.user_tasks()
        self.assertEqual(len(tasks), 2)

    def test_creates_inner_task(self):
        task_id = self.tasks_controller.create(self.task).id
        inner_task = self.tasks_controller.create_inner_task(
            task_id, self.task)
        self.assertEqual(inner_task.parent_task_id, task_id)

    def test_returns_inner_tasks(self):
        self.task.parent_task_id = None
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.create_inner_task(task_id, self.task)
        self.tasks_controller.create_inner_task(task_id, self.task)
        inner_tasks = self.tasks_controller.inner(task_id)
        self.assertEqual(len(inner_tasks), 2)

    def test_assignes_task_on_user(self):
        user_id = 5
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.assign_task_on_user(task_id, user_id)
        self.assertEqual(
            Task.select().where(
                Task.assigned_user_id == user_id).count(), 1)

    def test_adds_user_for_read(self):
        user_id = 5
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.add_user_for_read(
            user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            1)

    def test_adds_user_for_write(self):
        user_id = 5
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.add_user_for_write(
            user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            1)

    def test_removes_user_for_read(self):
        user_id = 5
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.add_user_for_read(
            user_id=user_id, task_id=task_id)
        self.tasks_controller.remove_user_for_read(
            user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersReadTasks.select().where(
                UsersReadTasks.task_id == task_id and UsersReadTasks.user_id == user_id).count(),
            0)

    def test_removes_user_for_write(self):
        user_id = 5
        task_id = self.tasks_controller.create(self.task).id
        self.tasks_controller.add_user_for_write(
            user_id=user_id, task_id=task_id)
        self.tasks_controller.remove_user_for_write(
            user_id=user_id, task_id=task_id)
        self.assertEqual(
            UsersWriteTasks.select().where(
                UsersWriteTasks.task_id == task_id and UsersWriteTasks.user_id == user_id).count(),
            0)

    # TaskPlansController tests

    def test_creates_task_plan(self):
        before_plans_count = TaskPlan.select().count()
        self.task_plans_controller.create(self.task_plan)
        after_plans_count = TaskPlan.select().count()
        self.assertEqual(before_plans_count + 1, after_plans_count)

    def test_deletes_task_plan_by_id(self):
        task_plan_id = self.task_plans_controller.create(self.task_plan).id
        self.task_plans_controller.delete(task_plan_id)
        self.assertEqual(TaskPlan.select().where(
            TaskPlan.id == task_plan_id).count(), 0)

    def test_updates_task_plan(self):
        new_interval = 500
        new_datetime = datetime.datetime.now()
        task_plan_with_id = self.task_plans_controller.create(self.task_plan)
        task_plan_with_id.interval = new_interval
        task_plan_with_id.last_created_at = new_datetime
        self.task_plans_controller.update(task_plan_with_id)
        task_plan_from_db = TaskPlan.get(TaskPlan.id == task_plan_with_id.id)
        self.assertEqual(task_plan_from_db.interval, new_interval)
        self.assertEqual(task_plan_from_db.last_created_at, new_datetime)

    def test_returns_all_user_plans(self):
        user_id = 10
        self.task_plan.user_id = 10
        plans_count = 3
        for i in range(plans_count):
            self.task_plans_controller.create(self.task_plan)
        plans = self.task_plans_controller.all()
        self.assertEqual(len(plans), plans_count)

    def test_processes_task_plans(self):
        user_id = 10
        repeated_task = TaskFactory()
        repeated_task.status = Status.TEMPLATE.value
        repeated_task.user_id = user_id
        task_id = self.tasks_controller.create(repeated_task).id
        before_tasks_count = len(self.tasks_controller.user_tasks())
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
        self.task_plans_controller.create(repeated_task_plan)
        self.task_plans_controller.create(repeated_task_plan_big_interval)
        self.task_plans_controller.process_plans(self.tasks_controller)
        self.assertEqual(len(self.tasks_controller.user_tasks()),
                         before_tasks_count + 1)

    # NotificationsController tests

    def test_creates_notification(self):
        before_notifications_count = Notification.select().count()
        self.notifications_controller.create(self.notification)
        after_notifications_count = Notification.select().count()
        self.assertEqual(
            before_notifications_count + 1,
            after_notifications_count)

    def test_deletes_notification_by_id(self):
        notification_id = self.notifications_controller.create(
            self.notification).id
        self.notifications_controller.delete(notification_id)
        self.assertEqual(Notification.select().where(
            Notification.id == notification_id).count(), 0)

    def test_updates_notification(self):
        new_title = "Updated title"
        notification_with_id = self.notifications_controller.create(
            self.notification)
        notification_with_id.title = new_title
        self.notifications_controller.update(notification_with_id)
        notification_from_db = Notification.get(
            Notification.id == notification_with_id.id)
        self.assertEqual(notification_from_db.title, new_title)

    def test_returns_all_user_notifications(self):
        user_id = 10
        self.notification.user_id = 10
        notifications_count = 3
        for i in range(notifications_count):
            self.notifications_controller.create(self.notification)
        notifications = self.notifications_controller.all()
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_pending_notifications(self):
        user_id = 10
        self.notification.user_id = 10
        self.notification.status = NotificationStatus.PENDING.value
        notifications_count = 3
        for i in range(notifications_count):
            self.notifications_controller.create(self.notification)
        # create notification with other status
        self.notification.status = NotificationStatus.CREATED.value
        self.notifications_controller.create(self.notification)
        notifications = self.notifications_controller.pending()
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_created_notifications(self):
        user_id = 10
        self.notification.user_id = 10
        self.notification.status = NotificationStatus.CREATED.value
        notifications_count = 3
        for i in range(notifications_count):
            self.notifications_controller.create(self.notification)
        # create notification with other status
        self.notification.status = NotificationStatus.PENDING.value
        self.notifications_controller.create(self.notification)
        notifications = self.notifications_controller.created()
        self.assertEqual(len(notifications), notifications_count)

    def test_returns_pending_notifications(self):
        user_id = 10
        self.notification.user_id = 10
        self.notification.status = NotificationStatus.SHOWN.value
        notifications_count = 3
        for i in range(notifications_count):
            self.notifications_controller.create(self.notification)
        # create notification with other status
        self.notification.status = NotificationStatus.CREATED.value
        self.notifications_controller.create(self.notification)
        notifications = self.notifications_controller.shown()
        self.assertEqual(len(notifications), notifications_count)

    def test_process_notification(self):
        self.task.start_time = datetime.datetime.now()
        task_id = self.tasks_controller.create(self.task).id
        relative_start_time = 300
        self.notification.status = NotificationStatus.CREATED.value
        self.notification.relative_start_time = 300
        self.notification.task_id = task_id
        notification_id = self.notifications_controller.create(
            self.notification).id
        self.notifications_controller.process_notifications()
        processed_notification = self.notifications_controller.get_by_id(
            notification_id)
        self.assertEqual(
            processed_notification.status,
            NotificationStatus.PENDING.value)

    def test_sets_notification_status_as_shown(self):
        notification_with_id = self.notifications_controller.create(
            self.notification)
        self.notifications_controller.set_as_shown(notification_with_id.id)
        notification_from_db = Notification.get(
            Notification.id == notification_with_id.id)
        self.assertEqual(
            notification_from_db.status,
            NotificationStatus.SHOWN.value)
