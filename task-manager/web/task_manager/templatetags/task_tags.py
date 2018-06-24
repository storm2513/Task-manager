from django import template
from django.conf import settings
from tmlib.controllers.categories_controller import create_categories_controller
from tmlib.controllers.tasks_controller import create_tasks_controller
from tmlib.models.task import Status, Priority
import tmlib.commands


register = template.Library()


def _create_categories_controller(user_id):
    return create_categories_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


def _create_tasks_controller(user_id):
    return create_tasks_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


@register.simple_tag
def get_category_name_by_id(user_id, id):
    category = tmlib.commands.get_category_by_id(
        _create_categories_controller(user_id), id)
    if category is None:
        return category
    return category.name


@register.simple_tag
def get_status(status):
    return Status(status).name


@register.simple_tag
def get_status_badge_class(status):
    classes = {'TODO': 'secondary',
               'IN_PROGRESS': 'primary',
               'DONE': 'success',
               'TEMPLATE': 'info'}
    return classes.get(Status(status).name, "")


@register.simple_tag
def get_priority(priority):
    return Priority(priority).name


@register.simple_tag
def get_priority_badge_class(priority):
    classes = {'MIN': 'secondary',
               'LOW': 'info',
               'MEDIUM': 'primary',
               'HIGH': 'warning',
               'MAX': 'danger'}
    return classes.get(Priority(priority).name, "")
