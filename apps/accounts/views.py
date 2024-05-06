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
    """Function based view for the user's dashboard"""

    user = request.user

    context = {
        "user_name": user.username,
        "user_email": user.email,
        "user_date_of_birth": user.date_of_birth,
    }

    return render(request, "registration/dashboard.html", context)
