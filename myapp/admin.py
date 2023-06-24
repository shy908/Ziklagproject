from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from myapp.models import CustomUser

class LogEntryAdmin(admin.ModelAdmin):
    # Other admin configurations...

    def get_user(self, obj):
        return obj.user

    get_user.short_description = 'User'
    get_user.admin_order_field = 'user'

    list_display = ['get_user', 'action_time', 'object_repr', 'change_message']

admin.site.register(LogEntry, LogEntryAdmin)
