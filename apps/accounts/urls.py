"""A module that contains all the urls for the accounts app."""

from django.urls import path

from apps.accounts.views import SignUpView, dashboard_view

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", dashboard_view, name="dashboard"),
]
