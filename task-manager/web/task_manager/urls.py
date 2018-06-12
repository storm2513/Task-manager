from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

app_name = "task_manager"

users_patterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'task_manager:home'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
]

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^users/', include(users_patterns)),
]