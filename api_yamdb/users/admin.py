from django.contrib import admin
from django.contrib.auth.models import Group

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
    )


admin.site.unregister(Group)
