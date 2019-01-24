from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.urls import include, path

from .views import index

# Customize Django Admin site
admin.site.site_header = _('Med database administration')
admin.site.site_title = _('Med Admin')

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('media/', include('media.urls')),
    path('search/', include('search.urls')),
    path('logs/', include('logs.urls')),
    path('', index, name="index"),
]
