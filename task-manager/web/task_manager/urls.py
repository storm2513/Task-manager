from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

app_name = "task_manager"

users_patterns = [
    url(r'^$', views.users, name='users'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'task_manager:home'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
]

categories_patterns = [
    url(r'^$', views.categories, name='categories'),
    url(r'^new/$', views.create_category, name='new_category'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_category, name='edit_category'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_category, name='delete_category'),
]

tasks_patterns = [
    url(r'^$', views.tasks, name='tasks'),
    url(r'^new/$', views.create_task, name='new_task'),
    url(r'^(?P<id>[0-9]+)/$', views.show_task, name='show_task'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_task, name='edit_task'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_task, name='delete_task'),
    url(r'^filter/assigned/$', views.assigned_tasks, name='assigned_tasks'),
    url(r'^filter/can_read/$', views.can_read_tasks, name='can_read_tasks'),
    url(r'^filter/can_write/$', views.can_write_tasks, name='can_write_tasks'),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^users/', include(users_patterns)),
    url(r'^categories/', include(categories_patterns)),
    url(r'^tasks/', include(tasks_patterns)),
]
