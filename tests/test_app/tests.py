"""Tests do not actually test django-mutpy, but are run by the tests for testing mutation testing (testception)."""

from unittest import TestCase

from test_app.calculator import mul


class BadCalculatorTest(TestCase):
    """Contains bad test cases, which do not uncover programming mistakes very well."""

    def test_mul(self):
        """Testing with the value '1' will not uncover operator substitutions."""
        self.assertEqual(mul(1, 1), 1)
