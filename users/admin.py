from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reversion.admin import VersionAdmin

from .models import User, Adhesion, Clef


@admin.register(Clef)
class ClefAdmin(VersionAdmin):
    list_display = ('proprio', 'nom')


@admin.register(Adhesion)
class AdhesionAdmin(VersionAdmin):
    list_display = ('annee_debut', 'annee_fin')


admin.site.register(User, UserAdmin)
