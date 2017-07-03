
from reversion.admin import VersionAdmin
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Auteur, Emprunt, Media

class AuteurAdmin(VersionAdmin):
    list_display = ('nom',)

class MediaAdmin(VersionAdmin):
    list_display = ('titre','cote')

class EmpruntAdmin(VersionAdmin):
    list_display = ('media','user','date_emprunt', 'date_rendu', 'permanencier_emprunt', 'permanencier_rendu')


admin.site.register(Auteur, AuteurAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Emprunt, EmpruntAdmin)