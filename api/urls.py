from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'media', views.MediaViewSet)
router.register(r'gametypes', views.GameTypeViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'keys', views.KeyViewSet)
router.register(r'memberships', views.MembershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/',
         include('rest_framework.urls', namespace='rest_framework'))
]
