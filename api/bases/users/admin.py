# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import (
    UserAdmin as _UserAdmin,
)
from django.contrib.auth.models import Permission
from django.contrib import admin
from django.utils import timezone

from .models import User, ExpiringToken


class UserAdmin(_UserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_filter = ('is_staff', 'is_active', 'groups', 'date_joined')
    list_display = ('email', 'is_staff', 'date_joined')
    search_fields = ('email',)
    ordering = ('email',)


class ExpiringTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created', 'updated', 'is_expired')
    actions = ('expire_token',)
    search_fields = ('user__email',)
    fields = ('user',)

    def is_expired(self, instance):
        return instance.expired()

    def expire_token(self, request, instance):
        instance.update(updated=timezone.now() - timezone.timedelta(days=1))

    is_expired.boolean = True
    expire_token.short_description = 'Expire selected Tokens'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'content_type__app_label',)
    list_filter = ('content_type',)


APP_NAME = 'Dummy API APP'
admin.site.site_header = f'{APP_NAME} Administration'
admin.site.site_title = f'{APP_NAME} Admin Portal'
admin.site.index_title = f'Welcome to {APP_NAME} Admin Portal'

admin.site.register(User, UserAdmin)

admin.site.register(ExpiringToken, ExpiringTokenAdmin)
