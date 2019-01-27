from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

# Customize Django Admin site
admin.site.site_header = _('Med database administration')
admin.site.site_title = _('Med Admin')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path('media/', include('media.urls')),
    path('search/', include('haystack.urls')),
    path('logs/', include('logs.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name="index"),
]
