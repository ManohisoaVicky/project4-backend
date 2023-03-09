from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.

from .models import CustomUser

class CustomUserAdmin(UserAdmin):

    model: CustomUser
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "bio"
    ]
    fieldsets = ((None, {"fields": ("username", "first_name", "last_name", "email", "bio",)}),)
    add_fieldsets = ((None, {"fields": ("username", "first_name", "last_name", "email", "bio",)}),)

admin.site.register(CustomUser, CustomUserAdmin)