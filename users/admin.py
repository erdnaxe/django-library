# Re2o est un logiciel d'administration développé initiallement au rezometz. Il
# se veut agnostique au réseau considéré, de manière à être installable en
# quelques clics.
#
# Copyright © 2017  Gabriel Détraz
# Copyright © 2017  Goulven Kermarec
# Copyright © 2017  Augustin Lemesle
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from reversion.admin import VersionAdmin

from .models import User, Right, Adhesion, ListRight, Clef, Request
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'pseudo',
        'email',
        'state'
    )
    search_fields = ('name','surname','pseudo')

class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'created_at', 'expires_at')

class RightAdmin(VersionAdmin):
    list_display = ('user', 'right')

class ClefAdmin(VersionAdmin):
    list_display = ('proprio', 'nom')

class AdhesionAdmin(VersionAdmin):
    list_display = ('annee_debut', 'annee_fin')

class ListRightAdmin(VersionAdmin):
    list_display = ('listright',)

class UserAdmin(VersionAdmin, BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('pseudo', 'name', 'surname', 'email', 'is_admin')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('pseudo', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'email')}),
        ('Permissions', {'fields': ('is_admin', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('pseudo', 'name', 'surname', 'email', 'is_admin', 'password1', 'password2')}
        ),
    )
    search_fields = ('pseudo',)
    ordering = ('pseudo',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(ListRight, ListRightAdmin)
admin.site.register(Right, RightAdmin)
admin.site.register(Adhesion, AdhesionAdmin)
admin.site.register(Clef, ClefAdmin)
# Now register the new UserAdmin...
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
