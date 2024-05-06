"""A module for auth page forms. They are later used in the views.py"""

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.accounts.models import CustomUser


# pylint: disable=too-few-public-methods
class CustomUserCreationForm(UserCreationForm):
    """A form for user creation"""

    class Meta:
        """Additional settings for the Meta?"""

        model = CustomUser
        fields = ("username", "email", "date_of_birth")

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )


# pylint: disable=too-few-public-methods
class CustomUserChangeForm(UserChangeForm):
    """A form for user change"""

    class Meta:
        """Additional settings for the Meta?"""

        model = CustomUser
        fields = ("username", "email", "date_of_birth")

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )
