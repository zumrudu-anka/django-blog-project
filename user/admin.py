from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class BlogUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profil", {"fields": ("avatar", "bio")}),
    )
