import datetime
from django import template
from django.conf import settings
from tmlib.controllers.tasks_controller import create_tasks_controller
from tmlib.models.notification import Status
import tmlib.commands


register = template.Library()


def _create_tasks_controller(user_id):
    return create_tasks_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


@register.simple_tag
def get_task_title_by_id(user_id, id):
    task = tmlib.commands.get_task_by_id(_create_tasks_controller(user_id), id)
    if task is None:
        return task
    return task.title


@register.simple_tag
def get_status(status):
    return Status(status).name


@register.simple_tag
def get_timedelta(seconds):
    return datetime.timedelta(seconds=seconds)
