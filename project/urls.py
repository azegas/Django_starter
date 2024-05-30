from django.contrib import admin
from django.urls import include, path

from project.views import Index, test

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", Index.as_view(), name="index"),
    path('test/', test, name="test"),
]
