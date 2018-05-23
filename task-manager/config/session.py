from storage.user_storage import UserStorage
from storage.task_storage import TaskStorage
from storage.level_storage import LevelStorage
from storage.category_storage import CategoryStorage
from storage.notification_storage import NotificationStorage
from controllers.categories_controller import CategoriesController
from controllers.levels_controller import LevelsController
from controllers.tasks_controller import TasksController
from controllers.users_controller import UsersController
from controllers.notifications_controller import NotificationsController
from models.user import User
from config.config_parser import *


def start_session():
    Controllers.TASKS = TasksController(TaskStorage())
    Controllers.USERS = UsersController(UserStorage())
    Controllers.LEVELS = LevelsController(LevelStorage())
    Controllers.CATEGORIES = CategoriesController(CategoryStorage())
    Controllers.NOTIFICATIONS = NotificationsController(NotificationStorage())
    authorize_user_from_config()
    if Global.USER is not None:
        Controllers.NOTIFICATIONS.process_notifications()


class Controllers:
    TASKS = None
    LEVELS = None
    USERS = None
    CATEGORIES = None
    NOTIFICATIONS = None


class Global:
    USER = None
