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
    url(r'^update/(?P<id>[0-9]+)/$', views.update_task, name='update_task'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_task, name='delete_task'),
    url(r'^assigned/$', views.assigned_tasks, name='assigned_tasks'),
    url(r'^can_read/$', views.can_read_tasks, name='can_read_tasks'),
    url(r'^can_write/$', views.can_write_tasks, name='can_write_tasks'),
    url(r'^category/(?P<id>[0-9]+)/$', views.tasks_by_category, name='tasks_by_category'),
    url(r'^status/(?P<id>[0-9]+)/$', views.tasks_by_status, name='tasks_by_status'),
    url(r'^priority/(?P<id>[0-9]+)/$', views.tasks_by_priority, name='tasks_by_priority'),
    url(r'^plan/(?P<id>[0-9]+)/$', views.tasks_by_plan, name='tasks_by_plan'),
]

notifications_patterns = [
    url(r'^$', views.notifications, name='notifications'),
    url(r'^new/(?P<id>[0-9]+)/$', views.create_notification, name='add_notification'),
    url(r'^all/$', views.all_notifications, name='all_notifications'),
    url(r'^created/$', views.created_notifications, name='created_notifications'),
    url(r'^pending/$', views.pending_notifications, name='pending_notifications'),
    url(r'^shown/$', views.shown_notifications, name='shown_notifications'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_notification, name='edit_notification'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_notification, name='delete_notification'),
    url(r'^set_as_shown/(?P<id>[0-9]+)/$', views.set_notification_as_shown, name='set_notification_as_shown'),
]

plans_patterns = [
    url(r'^templates/$', views.templates, name='templates'),
    url(r'^templates/new$', views.create_template_task, name='new_template'),
    url(r'^$', views.plans, name='plans'),
    url(r'^new/$', views.create_plan, name='new_plan'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_plan, name='edit_plan'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete_plan, name='delete_plan'),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^users/', include(users_patterns)),
    url(r'^categories/', include(categories_patterns)),
    url(r'^tasks/', include(tasks_patterns)),
    url(r'^notifications/', include(notifications_patterns)),
    url(r'^plans/', include(plans_patterns))
]
