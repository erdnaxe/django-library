from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.urls import include, path

from .views import index

# Customize Django Admin site
admin.site.site_header = _('Med administration')
admin.site.site_title = _('Med Admin')

urlpatterns = [
    url(r'^$', index),
    url('^logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'^media/', include('media.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^logs/', include('logs.urls')),
]
