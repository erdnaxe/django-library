from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reversion.admin import VersionAdmin

from .models import User, Adhesion, Clef


@admin.register(Clef)
class ClefAdmin(VersionAdmin):
    list_display = ('owner', 'name')


@admin.register(Adhesion)
class AdhesionAdmin(VersionAdmin):
    list_display = ('start_at', 'end_at', 'members_list')

    @staticmethod
    def members_list(obj):
        return "\n".join(p.get_full_name() for p in obj.member.all())


admin.site.register(User, UserAdmin)
