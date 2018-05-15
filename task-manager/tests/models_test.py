import unittest
import datetime

from models.task import Task
from models.level import Level
from models.user import User
from models.category import Category


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

    def create_level(self, id=1, experience=1):
        return Level(id=id, experience=experience)

    def test_level_creation(self):
        level = self.create_level()
        self.assertIsInstance(level, Level)

    def test_current_level_method(self):
        level_with_1_xp = self.create_level(id=1, experience=1)
        self.assertEqual(level_with_1_xp.current_level(), 1)
        level_with_10_xp = self.create_level(id=1, experience=10)
        self.assertEqual(level_with_10_xp.current_level(), 4)

    def test_next_level_experience_method(self):
        level_with_1_xp = self.create_level(id=1, experience=1)
        self.assertEqual(level_with_1_xp.next_level_experience(), 3)
        level_with_10_xp = self.create_level(id=1, experience=10)
        self.assertEqual(level_with_10_xp.next_level_experience(), 15)

    def create_user(
            self,
            email="email@example.com",
            name="Somename",
            password="somepassword"):
        self.user_email = email
        self.user_name = name
        self.user_password = password
        return User(email=email, name=name, password=password)

    def test_user_creation(self):
        user = self.create_user()
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.user_email)
        self.assertEqual(user.name, self.user_name)
        self.assertEqual(user.password, self.user_password)

    def create_category(self, name="Some category"):
        self.category_name = name
        return Category(name)

    def test_category_creation(self):
        category = self.create_category()
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, self.category_name)
