from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Reviewer

class ReviewerInline(admin.StackedInline):
    model = Reviewer
    # can_delete = False
    # verbose_name_plural = 'user'
class UserAdmin(BaseUserAdmin):
    inlines = (ReviewerInline,)

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)