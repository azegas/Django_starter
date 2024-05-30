"""A module for accounts app views."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Generic CBV view for account create page"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def dashboard_view(request):

    # Get the logged-in user
    user = request.user

    # # Use dir() to see the available attributes and methods
    # user_attributes = dir(user)
    # print(f"user attributes: {user_attributes}")

    # # Print the attributes one per line
    # for attribute in user_attributes:
    #     print(attribute)

    context = {
        "user_id": user.id,
        "user_password": user.password,
        "user_last_login": user.last_login,
        "user_is_superuser": user.is_superuser,
        "user_name": user.username,
        "user_fist_name": user.first_name,
        "user_last_name": user.last_name,
        "user_email": user.email,
        "user_is_staff": user.is_staff,
        "user_is_active": user.is_active,
        "user_date_joined": user.date_joined,
        "user_date_of_birth": user.date_of_birth,
    }

    return render(request, "registration/dashboard.html", context)
