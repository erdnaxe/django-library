from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from reversion.admin import VersionAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, Right, Adhesion, ListRight, Clef, Request


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'created_at', 'expires_at')


@admin.register(Right)
class RightAdmin(VersionAdmin):
    list_display = ('user', 'right')


@admin.register(Clef)
class ClefAdmin(VersionAdmin):
    list_display = ('proprio', 'nom')


@admin.register(Adhesion)
class AdhesionAdmin(VersionAdmin):
    list_display = ('annee_debut', 'annee_fin')


@admin.register(ListRight)
class ListRightAdmin(VersionAdmin):
    list_display = ('listright',)


@admin.register(User)
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
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'pseudo', 'name', 'surname', 'email', 'is_admin', 'password1',
                'password2')}
         ),
    )
    search_fields = ('pseudo',)
    ordering = ('pseudo',)
    filter_horizontal = ()
