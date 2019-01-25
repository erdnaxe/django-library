from django.urls import path

from . import views

app_name = 'logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:revision_id>/revert/', views.revert_action, name='revert'),
    path('stats/', views.stats_actions, name='stats'),
]
