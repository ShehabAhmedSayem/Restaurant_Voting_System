from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.admin import TokenAdmin as BaseTokenAdmin
from rest_framework.authtoken.models import TokenProxy

from user.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['username', 'user_type', 'is_active', 'is_staff']
    fieldsets = [
        [None, {'fields': ['username', 'password']}],
        [_('Permissions'), {
            'fields': [
                'user_type',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ],
        }],
        [_('Important dates'), {'fields': ['last_login', 'date_joined']}],
    ]
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups', 'user_type'
    )


class TokenAdmin(BaseTokenAdmin):
    raw_id_fields = ['user']


class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_id',
        'action_flag',
        'change_message',
        'user',
        'action_time'
    ]
    list_filter = ['action_flag', 'content_type']
    readonly_fields = (
        'content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        return actions


admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Permission)
admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, TokenAdmin)
