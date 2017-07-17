"""Tests do not actually test django-mutpy, but are run by the tests for testing mutation testing (testception)."""

from django.test import TestCase

from test_app_db.models import SingletonModel


class SingletonModelTest(TestCase):
    """Try to save to instances of the same model in two different test cases."""

    def test_save(self):
        """Save the singleton model instance."""
        model = SingletonModel()
        model.save()

    def test_save_again(self):
        """Save the singleton model instance a second time."""
        model = SingletonModel()
        model.save()
