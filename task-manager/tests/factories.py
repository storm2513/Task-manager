import factory
import factory.fuzzy
import datetime
from lib.models.task import Task as TaskInstance
from lib.models.category import Category as CategoryInstance
from lib.models.task_plan import TaskPlan as TaskPlanInstance
from lib.models.notification import Notification as NotificationInstance


class CategoryFactory(factory.Factory):
    class Meta:
        model = CategoryInstance

    name = factory.Faker('word')


class TaskFactory(factory.Factory):
    class Meta:
        model = TaskInstance

    title = factory.Faker('word')
    note = factory.Faker('word')
    user_id = 10


class TaskPlanFactory(factory.Factory):
    class Meta:
        model = TaskPlanInstance

    interval = factory.fuzzy.FuzzyInteger(300, 1000000, step=50)
    user_id = 10
    task_id = 10
    last_created_at = datetime.datetime.now()


class NotificationFactory(factory.Factory):
    class Meta:
        model = NotificationInstance

    title = factory.Faker('word')
    user_id = 10
    task_id = 10
    relative_start_time = factory.fuzzy.FuzzyInteger(300, 1000000, step=50)
