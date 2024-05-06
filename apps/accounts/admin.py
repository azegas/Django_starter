"""A module to register users app models to django admin."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """A modification to the default account model admin."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "date_of_birth")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = [
        "email",
        "username",
        "date_of_birth",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
