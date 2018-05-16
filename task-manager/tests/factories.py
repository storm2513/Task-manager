import factory
from models.user import User as UserInstance
from models.level import Level as LevelInstance
from models.task import Task as TaskInstance
from models.category import Category as CategoryInstance


class UserFactory(factory.Factory):
    class Meta:
        model = UserInstance

    email = factory.Faker('email')
    name = factory.Faker('first_name')
    password = factory.Faker('password')
    level_id = 10


class LevelFactory(factory.Factory):
    class Meta:
        model = LevelInstance


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
