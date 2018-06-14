from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.conf import settings
from tmlib.controllers.categories_controller import create_categories_controller
from tmlib.controllers.tasks_controller import create_tasks_controller
from tmlib.models.category import Category
from tmlib.models.task import Task, Status, Priority
import tmlib.commands
from .forms import CategoryForm, TaskForm


def home(request):
    username = 'stranger'
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'home.html', {'username': username})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('task_manager:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html',
                  {'form': form, 'username': request.user.username})


def users(request):
    users = User.objects.all()
    return render(request,
                  'users/index.html',
                  {'users': users,
                   'username': request.user.username,
                   'nav_bar': 'users'})


def _create_categories_controller(user_id):
    return create_categories_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


def _create_tasks_controller(user_id):
    return create_tasks_controller(
        user_id, settings.TASK_MANAGER_DATABASE_PATH)


@login_required
def categories(request):
    categories_controller = _create_categories_controller(request.user.id)
    categories = tmlib.commands.user_categories(categories_controller)
    return render(request,
                  'categories/index.html',
                  {'categories': categories,
                   'username': request.user.username,
                   'nav_bar': 'categories'})


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
                   'username': request.user.username,
                   'nav_bar': 'categories'})


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
                   'username': request.user.username,
                   'nav_bar': 'categories'})


@login_required
def delete_category(request, id):
    if request.method == 'POST':
        categories_controller = _create_categories_controller(request.user.id)
        tmlib.commands.delete_category(categories_controller, id)
    return redirect('task_manager:categories')


@login_required
def tasks(request):
    tasks_controller = _create_tasks_controller(request.user.id)
    tasks = tmlib.commands.user_tasks(tasks_controller)

    def get_task_category(id): return tmlib.commands.get_category_by_id(
        tasks_controller, id)
    return render(request,
                  'tasks/index.html',
                  {'tasks': tasks,
                   'username': request.user.username,
                   'nav_bar': 'tasks',
                   'user_id': request.user.id})


@login_required
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
            tmlib.commands.add_task(tasks_controller, task)
            return redirect('task_manager:tasks')
    else:
        form = TaskForm(request.user.id)
    return render(request,
                  'tasks/new.html',
                  {'form': form.as_p,
                   'username': request.user.username,
                   'nav_bar': 'tasks'})


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
    inner_tasks = tmlib.commands.get_inner_tasks(tasks_controller, task.id)

    return render(request,
                  'tasks/show.html',
                  {'username': request.user.username,
                   'nav_bar': 'tasks',
                   'task': task,
                   'category': category,
                   'priority': Priority(task.priority).name,
                   'status': Status(task.status).name,
                   'parent_task_title': parent_task_title,
                   'assigned_user': assigned_user,
                   'inner_tasks': inner_tasks})


@login_required
def edit_task(request, id):
    tasks_controller = _create_tasks_controller(request.user.id)
    task = tmlib.commands.get_task_by_id(tasks_controller, id)
    if task is None:
        return redirect('task_manager:tasks')
    if request.method == 'POST':
        form = TaskForm(request.user.id, request.POST)
        if form.is_valid():
            task.title = form.cleaned_data['title']
            task.note = form.cleaned_data['note']
            task.category_id = form.cleaned_data['category']
            task.priority = form.cleaned_data['priority']
            task.status = form.cleaned_data['status']
            task.is_event = form.cleaned_data['event']
            task.start_time = form.cleaned_data['start_time']
            task.end_time = form.cleaned_data['end_time']
            parent_task_id = form.cleaned_data['parent_task']
            task.parent_task_id = None if not parent_task_id else parent_task_id
            assigned_user = form.cleaned_data['assigned_user']
            task.assigned_user_id = assigned_user.id if assigned_user is not None else None
            tmlib.commands.update_task(tasks_controller, task)
            return redirect('task_manager:tasks')
    else:
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
                'assigned_user': task.assigned_user_id})
    return render(request,
                  'tasks/edit.html',
                  {'form': form.as_p,
                   'username': request.user.username,
                   'nav_bar': 'tasks'})


@login_required
def delete_task(request, id):
    if request.method == 'POST':
        tasks_controller = _create_tasks_controller(request.user.id)
        tmlib.commands.delete_task(tasks_controller, id)
    return redirect('task_manager:tasks')
