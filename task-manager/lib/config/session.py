from lib.storage.user_storage import UserStorage
from lib.storage.task_storage import TaskStorage
from lib.storage.level_storage import LevelStorage
from lib.storage.category_storage import CategoryStorage
from lib.storage.notification_storage import NotificationStorage
from lib.storage.task_plan_storage import TaskPlanStorage
from lib.controllers.categories_controller import CategoriesController
from lib.controllers.levels_controller import LevelsController
from lib.controllers.tasks_controller import TasksController
from lib.controllers.users_controller import UsersController
from lib.controllers.notifications_controller import NotificationsController
from lib.controllers.task_plans_controller import TaskPlansController
from lib.models.user import User
from lib.config.config_parser import *


def start_session():
    """
    Initializes controllers, authorizes user from config
    """

    Controllers.TASKS = TasksController(TaskStorage())
    Controllers.USERS = UsersController(UserStorage())
    Controllers.LEVELS = LevelsController(LevelStorage())
    Controllers.CATEGORIES = CategoriesController(CategoryStorage())
    Controllers.NOTIFICATIONS = NotificationsController(NotificationStorage())
    Controllers.TASK_PLANS = TaskPlansController(TaskPlanStorage())
    authorize_user_from_config()
    if Global.USER is not None:
        Controllers.NOTIFICATIONS.process_notifications()
        Controllers.TASK_PLANS.process_plans()


class Controllers:
    TASKS = None
    LEVELS = None
    USERS = None
    CATEGORIES = None
    NOTIFICATIONS = None
    TASK_PLANS = None


class Global:
    USER = None
