import datetime
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from tmlib.controllers.categories_controller import create_categories_controller
from tmlib.controllers.tasks_controller import create_tasks_controller
import tmlib.commands
from tmlib.models.task import Status, Priority
from tmlib.storage.storage_models import Task
from tempus_dominus.widgets import DateTimePicker


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100)


class TaskForm(forms.Form):
    def __init__(self, user_id=None, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        categories = tmlib.commands.user_categories(
            create_categories_controller(
                user_id, settings.TASK_MANAGER_DATABASE_PATH))
        categories_tuple = [(category.id, category.name)
                            for category in categories]
        tasks = tmlib.commands.filter_tasks(
            create_tasks_controller(
                user_id,
                settings.TASK_MANAGER_DATABASE_PATH),
            (Task.status != Status.TEMPLATE.value) & (Task.user_id == user_id))
        tasks_tuple = [(task.id, task.title) for task in tasks]
        tasks_tuple.insert(0, ('', '---------'))  # required for default value
        self.fields['category'] = forms.ChoiceField(
            choices=categories_tuple, required=False)
        self.fields['parent_task'] = forms.ChoiceField(
            choices=tasks_tuple, required=False)

    title = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'placeholder': 'Your amazing task title'}))
    note = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Your amazing note'}))
    category = forms.ChoiceField(required=False)
    status = forms.ChoiceField(
        choices=[(e.value, Status(e).name) for e in Status])
    priority = forms.ChoiceField(
        choices=[(e.value, Priority(e).name) for e in Priority])
    event = forms.BooleanField(initial=False, required=False)
    start_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (datetime.date.today()).strftime('%Y-%m-%d'),
                'useCurrent': True,
            }
        ), required=False
    )
    end_time = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (
                    datetime.date.today() +
                    datetime.timedelta(
                        days=1)).strftime('%Y-%m-%d'),
                'useCurrent': False,
            }),
        required=False)
    parent_task = forms.ChoiceField()
    assigned_user = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False)
    can_read = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False)
    can_write = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(), required=False)


class TaskFormWithoutStatus(TaskForm):
    def __init__(self, *args, **kwargs):
        super(TaskFormWithoutStatus, self).__init__(*args, **kwargs)
        self.fields.pop('status')


class NotificationForm(forms.Form):
    title = forms.CharField(max_length=200)
    relative_start_time = forms.CharField(max_length=50)


class PlanForm(forms.Form):
    def __init__(self, user_id=None, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)

        tasks = tmlib.commands.filter_tasks(
            create_tasks_controller(
                user_id, settings.TASK_MANAGER_DATABASE_PATH),
            (Task.status == Status.TEMPLATE.value) & (Task.user_id == user_id))
        tasks_tuple = [(task.id, task.title) for task in tasks]
        self.fields['task_template'] = forms.ChoiceField(
            choices=tasks_tuple, required=False)

    task_template = forms.ChoiceField(required=False)
    interval = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': '1 day'}),
        required=False)
    last_created_at = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (datetime.date.today()).strftime('%Y-%m-%d'),
                'useCurrent': True,
            }
        ), required=False
    )
