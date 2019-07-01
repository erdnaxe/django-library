from django.urls import path

from . import views

app_name = 'logs'
urlpatterns = [
    path('', views.LogsIndex.as_view(), name='index'),
    path('stats/', views.StatsIndex.as_view(), name='stats'),
    # path('<int:revision_id>/revert/', views.revert_action, name='revert'),
]
