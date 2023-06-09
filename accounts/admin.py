from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'display_name', 'is_staff']
    fieldsets = (
        ('Main', {'fields': ('username', 'email', 'password')}),
        ('Others', {'fields': ('display_name', 'bio', 'is_reviewer', 'is_moderator')}),

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)

    