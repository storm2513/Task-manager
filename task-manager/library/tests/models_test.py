import unittest
import datetime

from tmlib.models.task import Task
from tmlib.models.category import Category
from tmlib.models.task_plan import TaskPlan
from tmlib.models.notification import Notification


class ModelsTest(unittest.TestCase):
    def create_task(self,
                    user_id=1,
                    title="Some title",
                    note="Some note",
                    id=1):
        self.task_title = title
        self.task_note = note
        return Task(user_id=1,
                    title=title,
                    note=note,
                    id=1)

    def test_task_creation(self):
        task = self.create_task()
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, self.task_title)
        self.assertEqual(task.note, self.task_note)

    def create_category(self, name="Some category"):
        self.category_name = name
        return Category(name)

    def test_category_creation(self):
        category = self.create_category()
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, self.category_name)

    def create_notification(
            self,
            task_id=1,
            title="Some title",
            relative_start_time="1 week"):
        self.task_id = task_id
        self.title = "Some title"
        self.relative_start_time = relative_start_time
        return Notification(
            task_id=task_id,
            title=title,
            relative_start_time=relative_start_time)

    def test_notification_creation(self):
        notification = self.create_notification()
        self.assertEqual(notification.task_id, self.task_id)
        self.assertEqual(notification.title, self.title)
        self.assertEqual(
            notification.relative_start_time,
            self.relative_start_time)

    def create_task_plan(self,
                         interval=500,
                         user_id=1,
                         task_id=1,
                         last_created_at=datetime.datetime.now()):
        self.interval = interval
        self.user_id = user_id
        self.task_id = task_id
        self.last_created_at = last_created_at
        return TaskPlan(
            interval=interval,
            user_id=user_id,
            task_id=task_id,
            last_created_at=last_created_at)

    def test_task_plan_creation(self):
        plan = self.create_task_plan()
        self.assertEqual(plan.interval, self.interval)
        self.assertEqual(plan.user_id, self.user_id)
        self.assertEqual(plan.task_id, self.task_id)
        self.assertEqual(plan.last_created_at, self.last_created_at)
