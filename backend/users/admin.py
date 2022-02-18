
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User


class UserAdmin(UserAdmin):
    exclude = ("username",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {"fields": (
                "is_active",
                "is_staff",
                "is_superuser"
            )},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
    )
    list_filter = (
        "is_superuser",
        "is_active",
    )
    ordering = ("email",)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
