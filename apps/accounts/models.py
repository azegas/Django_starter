"""A module to register account app models to django admin."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Account model."""

    date_of_birth = models.DateField(null=True, blank=True)
