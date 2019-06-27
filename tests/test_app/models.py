"""Contains Django models."""

from django.db import models


class SingletonModel(models.Model):
    """This model can only be saved once, if unaltered.

    It is used to test the test isolation regarding the database.
    """
    unique_field = models.BooleanField(default=True, unique=True)
