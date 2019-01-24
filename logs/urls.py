from django.urls import path, re_path

from . import views

app_name = 'logs'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^revert_action/(?P<revision_id>[0-9]+)$', views.revert_action,
            name='revert-action'),
    path('stats_actions/', views.stats_actions, name='stats-actions'),
]
