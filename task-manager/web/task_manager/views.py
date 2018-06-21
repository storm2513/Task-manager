import datetime
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.conf import settings
from tmlib.controllers.categories_controller import create_categories_controller
from tmlib.controllers.tasks_controller import create_tasks_controller
from tmlib.controllers.notifications_controller import create_notifications_controller
from tmlib.controllers.task_plans_controller import create_task_plans_controller
from tmlib.models.category import Category
from tmlib.models.task import Task, Status, Priority
from tmlib.models.notification import Notification, Status as NotificationStatus
from tmlib.models.task_plan import TaskPlan
from tmlib.storage.storage_models import Task as TaskFilter
import tmlib.commands
from pytimeparse import parse
from .forms import CategoryForm, TaskForm, TaskFormWithoutStatus, NotificationForm, PlanForm
from .models import Level


def home(request):
    username = 'stranger'
    if request.user.is_authenticated():
        username = request.user.username
    return render(
        request, 'home.html',
        {'username': username,
         'pending_notifications': _get_pending_notifications(request.user.id)})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Level.objects.create(user_id=user.id, experience=0)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('task_manager:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def users(request):
    users = User.objects.all()
    return render(request,
                  'users/index.html',
                  {'users': users,
                   'user': request.user,
                   'nav_bar': 'users',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


def _create_categories_controller(user_id):
    return create_categories_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


def _create_tasks_controller(user_id):
    return create_tasks_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


def _create_task_plans_controller(user_id):
    return create_task_plans_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


def _create_notifications_controller(user_id):
    return create_notifications_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


def _get_pending_notifications(user_id):
    notifications_controller = _create_notifications_controller(user_id)
    return tmlib.commands.pending_notifications(notifications_controller)


def process_plans(function):
    def wrap(request, *args, **kwargs):
        _create_task_plans_controller(
            request.user.id).process_plans(_create_tasks_controller(
                request.user.id))
        return function(request, *args, **kwargs)
    return wrap


@login_required
def categories(request):
    categories_controller = _create_categories_controller(request.user.id)
    categories = tmlib.commands.user_categories(categories_controller)
    return render(request,
                  'categories/index.html',
                  {'categories': categories,
                   'user': request.user,
                   'nav_bar': 'categories',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = Category(name)
            categories_controller = _create_categories_controller(
                request.user.id)
            tmlib.commands.add_category(categories_controller, category)
            return redirect('task_manager:categories')
    else:
        form = CategoryForm()
    return render(request,
                  'categories/new.html',
                  {'form': form,
                   'user': request.user,
                   'nav_bar': 'categories',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
def edit_category(request, id):
    categories_controller = _create_categories_controller(request.user.id)
    category = tmlib.commands.get_category_by_id(categories_controller, id)
    if category is None:
        return redirect('task_manager:categories')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category.name = form.cleaned_data['name']
            tmlib.commands.update_category(categories_controller, category)
            return redirect('task_manager:categories')
    else:
        form = CategoryForm(initial={'name': category.name})
    return render(request,
                  'categories/edit.html',
                  {'form': form,
                   'user': request.user,
                   'nav_bar': 'categories',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
def delete_category(request, id):
    if request.method == 'POST':
        categories_controller = _create_categories_controller(request.user.id)
        tmlib.commands.delete_category(categories_controller, id)
    return redirect('task_manager:categories')


@login_required
@process_plans
def tasks(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.filter_tasks(
        tasks_controller,
        TaskFilter.status != Status.TEMPLATE.value)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'My tasks',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def tasks_by_category(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.filter_tasks(
        tasks_controller, TaskFilter.category_id == int(id))
    categories_controller = _create_categories_controller(request.user.id)
    category = tmlib.commands.get_category_by_id(categories_controller, id)
    query = '?category={}'.format(id)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Tasks with category "{}"'.format(category.name),
                   'query': query,
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def tasks_by_status(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.filter_tasks(
        tasks_controller, TaskFilter.status == int(id))
    query = '?status={}'.format(id)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Tasks with status "{}"'.format(Status(int(id)).name),
                   'query': query,
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def tasks_by_priority(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.filter_tasks(
        tasks_controller, TaskFilter.priority == int(id))
    query = '?priority={}'.format(id)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Tasks with priority "{}"'.format(Priority(int(id)).name),
                   'query': query,
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def tasks_by_plan(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.filter_tasks(
        tasks_controller, TaskFilter.plan_id == int(id))
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Tasks created by plan with ID {}'.format(id),
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def assigned_tasks(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.assigned_tasks(tasks_controller)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Assigned on me tasks',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def can_read_tasks(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.can_read_tasks(tasks_controller)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Other tasks that I can read',
                   'view': 'can_read',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def can_write_tasks(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.can_write_tasks(tasks_controller)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'header': 'Other tasks that I can write',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.user.id, request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            note = form.cleaned_data['note']
            category_id = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            status = form.cleaned_data['status']
            is_event = form.cleaned_data['event']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            parent_task_id = form.cleaned_data['parent_task']
            parent_task_id = None if not parent_task_id else parent_task_id
            assigned_user = form.cleaned_data['assigned_user']
            assigned_user_id = assigned_user.id if assigned_user is not None else None
            task = Task(
                title=title,
                note=note,
                category_id=category_id,
                priority=priority,
                status=status,
                is_event=is_event,
                start_time=start_time,
                end_time=end_time,
                parent_task_id=parent_task_id,
                assigned_user_id=assigned_user_id)
            tasks_controller = _create_tasks_controller(request.user.id)
            task.id = tmlib.commands.add_task(tasks_controller, task).id
            can_read_users = form.cleaned_data['can_read']
            can_write_users = form.cleaned_data['can_write']
            tmlib.commands.remove_all_users_for_read(tasks_controller, task.id)
            if can_read_users is not None:
                user_ids = [user.id for user in can_read_users]
                for user_id in user_ids:
                    tmlib.commands.add_user_for_read(
                        tasks_controller, user_id, task.id)
            tmlib.commands.remove_all_users_for_write(
                tasks_controller, task.id)
            if can_write_users is not None:
                user_ids = [user.id for user in can_write_users]
                for user_id in user_ids:
                    tmlib.commands.add_user_for_write(
                        tasks_controller, user_id, task.id)
            return redirect('task_manager:tasks')
    else:
        initial = {
            'status': Status.TODO.value,
            'priority': Priority.MEDIUM.value}
        if request.GET.get('category') is not None:
            initial['category'] = request.GET.get('category')
        if request.GET.get('status') is not None:
            initial['status'] = request.GET.get('status')
        if request.GET.get('priority') is not None:
            initial['priority'] = request.GET.get('priority')
        form = TaskForm(request.user.id, initial)
    return render(request,
                  'tasks/new.html',
                  {'form': form.as_p,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
def show_task(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    task = tmlib.commands.get_task_by_id(tasks_controller, id)
    if task is None:
        return redirect('task_manager:tasks')
    category = tmlib.commands.get_category_by_id(
        _create_categories_controller(
            request.user.id), task.category_id)
    parent_task_title = None
    if task.parent_task_id is not None:
        parent_task = tmlib.commands.get_task_by_id(
            tasks_controller, task.parent_task_id)
        if parent_task is not None:
            parent_task_title = parent_task.title
    assigned_user = None
    if task.assigned_user_id is not None:
        try:
            assigned_user = User.objects.get(id=task.assigned_user_id).username
        except User.DoesNotExist:
            pass
    inner_tasks = tmlib.commands.get_inner_tasks(
        tasks_controller, task.id, recursive=True)
    creator = User.objects.get(id=task.user_id)

    return render(request,
                  'tasks/show.html',
                  {'user': request.user,
                   'nav_bar': 'tasks',
                   'task': task,
                   'category': category,
                   'priority': Priority(task.priority).name,
                   'status': Status(task.status).name,
                   'parent_task_title': parent_task_title,
                   'assigned_user': assigned_user,
                   'inner_tasks': inner_tasks,
                   'creator': creator.username,
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def edit_task(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    task = tmlib.commands.get_task_by_id(tasks_controller, id)
    if task is None or not tmlib.commands.user_can_write_task(
            tasks_controller, id):
        return redirect('task_manager:tasks')
    if request.method == 'POST':
        form = TaskForm(request.user.id, request.POST)
        if form.is_valid():
            task.title = form.cleaned_data['title']
            task.note = form.cleaned_data['note']
            task.category_id = form.cleaned_data['category']
            task.priority = form.cleaned_data['priority']
            previous_status = task.status
            task.status = int(form.cleaned_data['status'])
            if previous_status == Status.IN_PROGRESS.value and task.status == Status.DONE.value:
                request.user.level.increase()
            task.is_event = form.cleaned_data['event']
            task.start_time = form.cleaned_data['start_time']
            task.end_time = form.cleaned_data['end_time']
            parent_task_id = form.cleaned_data['parent_task']
            task.parent_task_id = None if not parent_task_id else parent_task_id
            assigned_user = form.cleaned_data['assigned_user']
            task.assigned_user_id = assigned_user.id if assigned_user is not None else None
            tmlib.commands.update_task(tasks_controller, task)
            can_read_users = form.cleaned_data['can_read']
            can_write_users = form.cleaned_data['can_write']
            tmlib.commands.remove_all_users_for_read(tasks_controller, task.id)
            if can_read_users is not None:
                user_ids = [user.id for user in can_read_users]
                for user_id in user_ids:
                    tmlib.commands.add_user_for_read(
                        tasks_controller, user_id, task.id)
            tmlib.commands.remove_all_users_for_write(
                tasks_controller, task.id)
            if can_write_users is not None:
                user_ids = [user.id for user in can_write_users]
                for user_id in user_ids:
                    tmlib.commands.add_user_for_write(
                        tasks_controller, user_id, task.id)
            return redirect('task_manager:tasks')
    else:
        users_can_read_ids = tmlib.commands.get_users_can_read_task(
            tasks_controller, id)
        users_can_write_ids = tmlib.commands.get_users_can_write_task(
            tasks_controller, id)
        can_read = User.objects.filter(id__in=users_can_read_ids)
        can_write = User.objects.filter(id__in=users_can_write_ids)
        form = TaskForm(
            request.user.id,
            initial={
                'title': task.title,
                'note': task.note,
                'status': task.status,
                'priority': task.priority,
                'category': task.category_id,
                'event': task.is_event,
                'start_time': task.start_time,
                'end_time': task.end_time,
                'parent_task': task.parent_task_id,
                'assigned_user': task.assigned_user_id,
                'can_read': can_read,
                'can_write': can_write})

    return render(request,
                  'tasks/edit.html',
                  {'form': form.as_p,
                   'user': request.user,
                   'nav_bar': 'tasks',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def delete_task(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    if request.method == 'POST' and tmlib.commands.user_can_write_task(
            tasks_controller, id):
        tmlib.commands.delete_task(tasks_controller, id)
    return redirect('task_manager:tasks')


def process_notifications(function):
    def wrap(request, *args, **kwargs):
        _create_notifications_controller(
            request.user.id).process_notifications()
        return function(request, *args, **kwargs)
    return wrap


@login_required
@process_notifications
@process_plans
def notifications(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks_with_start_time = tmlib.commands.filter_tasks(
        tasks_controller, TaskFilter.start_time > datetime.datetime.now())
    return render(request,
                  'notifications/tasks.html',
                  {'tasks': tasks_with_start_time,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def create_notification(request, id):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        str_relative_start_time = form.data['relative_start_time']
        relative_start_time = parse(str_relative_start_time)
        if relative_start_time is None:
            form.add_error(None, "Relative start time is incorrect")
        if form.is_valid():
            title = form.cleaned_data['title']
            notifications_controller = _create_notifications_controller(
                request.user.id)
            tasks_controller = _create_tasks_controller(request.user.id)
            notification = Notification(
                title=title,
                relative_start_time=relative_start_time,
                user_id=request.user.id,
                task_id=id)
            tmlib.commands.add_notification(
                tasks_controller, notifications_controller, notification)
            return redirect('task_manager:all_notifications')
    else:
        form = NotificationForm()
    return render(request,
                  'notifications/new.html',
                  {'form': form,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def edit_notification(request, id):
    notifications_controller = _create_notifications_controller(
        request.user.id)
    notification = tmlib.commands.get_notification_by_id(
        notifications_controller, id)
    if notification is None:
        return redirect('task_manager:all_notifications')
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        str_relative_start_time = form.data['relative_start_time']
        relative_start_time = parse(str_relative_start_time)
        if relative_start_time is None:
            form.add_error(None, "Relative start time is incorrect")
        if form.is_valid():
            notification.title = form.cleaned_data['title']
            notification.relative_start_time = relative_start_time
            tasks_controller = _create_tasks_controller(request.user.id)
            tmlib.commands.update_notification(
                tasks_controller, notifications_controller, notification)
            return redirect('task_manager:all_notifications')
    else:
        form = NotificationForm(
            initial={
                'title': notification.title,
                'relative_start_time': datetime.timedelta(
                    seconds=notification.relative_start_time)})
    return render(request,
                  'notifications/edit.html',
                  {'form': form,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def all_notifications(request):
    notifications_controller = _create_notifications_controller(
        request.user.id)
    notifications = tmlib.commands.user_notifications(notifications_controller)
    return render(request,
                  'notifications/index.html',
                  {'notifications': notifications,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'header': 'All notifications',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def created_notifications(request):
    notifications_controller = _create_notifications_controller(
        request.user.id)
    notifications = tmlib.commands.user_created_notifications(
        notifications_controller)
    return render(request,
                  'notifications/index.html',
                  {'notifications': notifications,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'header': 'Created notifications',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def pending_notifications(request):
    notifications_controller = _create_notifications_controller(
        request.user.id)
    notifications = tmlib.commands.pending_notifications(
        notifications_controller)
    return render(request,
                  'notifications/index.html',
                  {'notifications': notifications,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'header': 'Pending notifications',
                   'view': 'pending',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def shown_notifications(request):
    notifications_controller = _create_notifications_controller(
        request.user.id)
    notifications = tmlib.commands.user_shown_notifications(
        notifications_controller)
    return render(request,
                  'notifications/index.html',
                  {'notifications': notifications,
                   'user': request.user,
                   'nav_bar': 'notifications',
                   'header': 'Shown notifications',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_notifications
def delete_notification(request, id):
    if request.method == 'POST':
        notifications_controller = _create_notifications_controller(
            request.user.id)
        tmlib.commands.delete_notification(notifications_controller, id)
    return redirect('task_manager:all_notifications')


@login_required
def set_notification_as_shown(request, id):
    if request.method == 'POST':
        notifications_controller = _create_notifications_controller(
            request.user.id)
        tmlib.commands.set_notification_as_shown(notifications_controller, id)
    return redirect('task_manager:all_notifications')


@login_required
def templates(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    all_tasks = tmlib.commands.user_tasks(tasks_controller)
    tasks = [task for task in all_tasks if task.status == Status.TEMPLATE.value]
    return render(request,
                  'plans/templates.html',
                  {'tasks': tasks,
                   'user': request.user,
                   'nav_bar': 'plans',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
def create_template_task(request):
    if request.method == 'POST':
        form = TaskFormWithoutStatus(request.user.id, request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            note = form.cleaned_data['note']
            category_id = form.cleaned_data['category']
            priority = form.cleaned_data['priority']
            is_event = form.cleaned_data['event']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            parent_task_id = form.cleaned_data['parent_task']
            parent_task_id = None if not parent_task_id else parent_task_id
            assigned_user = form.cleaned_data['assigned_user']
            assigned_user_id = assigned_user.id if assigned_user is not None else None
            task = Task(
                title=title,
                note=note,
                category_id=category_id,
                priority=priority,
                status=Status.TEMPLATE.value,
                is_event=is_event,
                start_time=start_time,
                end_time=end_time,
                parent_task_id=parent_task_id,
                assigned_user_id=assigned_user_id)
            tasks_controller = _create_tasks_controller(request.user.id)
            task.id = tmlib.commands.add_task(tasks_controller, task).id
            can_read_users = form.cleaned_data['can_read']
            can_write_users = form.cleaned_data['can_write']
            tmlib.commands.remove_all_users_for_read(tasks_controller, task.id)
            if can_read_users is not None:
                user_ids = [user.id for user in can_read_users]
                for user_id in user_ids:
                    tmlib.commands.add_user_for_read(
                        tasks_controller, user_id, task.id)
            tmlib.commands.remove_all_users_for_write(
                tasks_controller, task.id)
            if can_write_users is not None:
                user_ids = [user.id for user in can_write_users]
                for user_id in user_ids:
                    tmlib.commands.add_user_for_write(
                        tasks_controller, user_id, task.id)
            return redirect('task_manager:templates')
    else:
        form = TaskFormWithoutStatus(request.user.id)
    return render(request,
                  'tasks/new.html',
                  {'form': form.as_p,
                   'user': request.user,
                   'nav_bar': 'plans',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def plans(request):
    task_plans_controller = _create_task_plans_controller(request.user.id)
    plans = tmlib.commands.get_task_plans(task_plans_controller)
    return render(request,
                  'plans/index.html',
                  {'plans': plans,
                   'user': request.user,
                   'nav_bar': 'plans',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def create_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.user.id, request.POST)
        str_interval = form.data['interval']
        interval = parse(str_interval)
        if interval is None:
            form.add_error(None, "Interval is incorrect")
        if interval < 300:  # 5 minutes
            form.add_error(None, "Interval should be more than 5 minutes")
        if form.is_valid():
            last_created_at = form.cleaned_data['last_created_at']
            if last_created_at is None:
                last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            task_id = int(form.cleaned_data['task_template'])
            task_plans_controller = _create_task_plans_controller(
                request.user.id)
            plan = TaskPlan(
                interval=interval,
                last_created_at=last_created_at,
                user_id=request.user.id,
                task_id=task_id)
            tmlib.commands.add_task_plan(
                task_plans_controller, plan)
            return redirect('task_manager:plans')
    else:
        initial = {}
        if request.GET.get('task_template') is not None:
            initial['task_template'] = request.GET.get('task_template')
        form = PlanForm(request.user.id, initial)
    return render(request,
                  'plans/new.html',
                  {'form': form.as_p,
                   'user': request.user,
                   'nav_bar': 'plans',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def edit_plan(request, id):
    task_plans_controller = _create_task_plans_controller(
        request.user.id)
    plan = tmlib.commands.get_task_plan_by_id(
        task_plans_controller, id)
    if plan is None:
        return redirect('task_manager:plans')
    if request.method == 'POST':
        form = PlanForm(request.user.id, request.POST)
        str_interval = form.data['interval']
        interval = parse(str_interval)
        if interval is None:
            form.add_error(None, "Interval is incorrect")
        if interval < 300:  # 5 minutes
            form.add_error(None, "Interval should be more than 5 minutes")
        if form.is_valid():
            last_created_at = form.cleaned_data['last_created_at']
            if last_created_at is None:
                last_created_at = datetime.datetime.now() - datetime.timedelta(seconds=interval)
            plan.last_created_at = last_created_at
            plan.interval = interval
            tmlib.commands.update_task_plan(
                task_plans_controller, plan)
            return redirect('task_manager:plans')
    else:
        form = PlanForm(request.user.id,
                        initial={
                            'last_created_at': plan.last_created_at,
                            'interval': datetime.timedelta(
                                seconds=plan.interval)})
    return render(request,
                  'plans/edit.html',
                  {'form': form.as_p,
                   'user': request.user,
                   'nav_bar': 'plans',
                   'pending_notifications': _get_pending_notifications(request.user.id)})


@login_required
@process_plans
def delete_plan(request, id):
    if request.method == 'POST':
        task_plans_controller = _create_task_plans_controller(
            request.user.id)
        tmlib.commands.delete_task_plan(task_plans_controller, id)
    return redirect('task_manager:plans')
