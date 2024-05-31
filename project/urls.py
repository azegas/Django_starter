from django.contrib import admin
from django.urls import include, path

from project.views import Index, test
from apps.dashboard.views import profile

urlpatterns = [
    path("administratorius/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", Index.as_view(), name="index"),
    path("accounts/profile/", profile, name="profile"),
    path("test/", test, name="test"),
]

from django.conf import settings

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
