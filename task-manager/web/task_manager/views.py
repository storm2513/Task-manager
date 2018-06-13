from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import CategoryForm

from tmlib.controllers.categories_controller import create_categories_controller
from tmlib.models.category import Category
import tmlib.commands


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


def _create_categories_controller(user_id):
    return create_categories_controller(
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
        form = CreateCategoryForm(request.POST)
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
    print(request)
    if request.method == 'POST':
        categories_controller = _create_categories_controller(request.user.id)
        tmlib.commands.delete_category(categories_controller, id)
    return redirect('task_manager:categories')
