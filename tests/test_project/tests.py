"""Tests for django-mutpy."""

import subprocess
import sys
from argparse import ArgumentParser
from contextlib import contextmanager
from io import StringIO
from unittest import TestCase, mock
from unittest.mock import MagicMock

from django.test import SimpleTestCase

from django_mutpy.management.commands.muttest import Command
from django_mutpy.mutpy_runner import run_mutpy_on_app
from django_mutpy.utils import list_all_modules_in_package


class Devnull(object):
    """Dummy output class which discards received output immediately."""

    def write(self, _):
        """Do nothing."""
        pass

    def flush(self):
        """Do nothing."""
        pass


@contextmanager
def captured_output():
    """Capture stdout and stderr."""
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout.getvalue().strip(), sys.stderr.getvalue().strip()
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@mock.patch('django_mutpy.management.commands.muttest.run_mutpy_on_app')
class MuttestCommandTest(SimpleTestCase):
    """Unit tests for the 'muttest' command class."""

    command = None

    def setUp(self):
        """Create an instance of the command class before each test."""
        self.command = Command(stdout=Devnull(), stderr=Devnull())
        self.command.requires_system_checks = False

    def run_command(self, args):
        """Run the 'muttest' command with some arguments."""
        self.command.run_from_argv(['tests.py', 'muttest'] + args)

    def suppress_output(self):
        """After calling this function, all output to stdout and stderr will be swallowed."""
        sys.stderr = Devnull()
        sys.stdout = Devnull()

    def test_wrong_apps(self, run_mutpy_on_app):
        """Try to execute the command on non-existing apps."""
        with self.modify_settings(
                INSTALLED_APPS={"prepend": ['app1', 'app2']}
        ):
            # when
            with self.assertRaises(SystemExit) as cm:
                self.run_command(['non_existing_app'])
                # then
            self.assertEqual(cm.exception.code, 1)

    def test_partially_wrong_apps(self, run_mutpy_on_app):
        """Try to execute the command on an existing and a non-existing app."""
        with self.modify_settings(
                INSTALLED_APPS={"prepend": ['app1', 'app2']}
        ):
            # when
            with self.assertRaises(SystemExit) as cm:
                self.run_command(['app2', 'non_existing_app'])
                # then
            self.assertEqual(cm.exception.code, 1)

    def test_too_many_apps(self, run_mutpy_on_app):
        """Try to execute the command on all existing and a non-existing app."""
        with self.modify_settings(
                INSTALLED_APPS={"prepend": ['app1', 'app2']}
        ):
            # when
            with self.assertRaises(SystemExit) as cm:
                self.run_command(['app1', 'app2', 'non_existing_app'])
                # then
            self.assertEqual(cm.exception.code, 1)

    def test_no_apps(self, run_mutpy_on_app):
        """Try to execute the command with no apps."""
        # when
        with self.assertRaises(SystemExit) as cm:
            self.suppress_output()
            self.run_command([])
            # then
        self.assertEqual(cm.exception.code, 2)

    def test_delegate_command_with_one_app(self, run_mutpy_on_app):
        """Check correct delegation to 'run_mutpy_on_app."""
        with self.modify_settings(
                INSTALLED_APPS={"prepend": ['app1', 'app2']}
        ):
            # when
            self.run_command(['app1'])
            # then
            run_mutpy_on_app.assert_called_once_with('app1', include_list=None)

    def test_delegate_command_with_two_apps(self, run_mutpy_on_app):
        """Check correct delegation to 'run_mutpy_on_app with two apps."""
        with self.modify_settings(
                INSTALLED_APPS={"prepend": ['app1', 'app2']}
        ):
            # when
            self.run_command(['app1', 'app2'])
            # then
            run_mutpy_on_app.assert_any_call('app1', include_list=None)
            run_mutpy_on_app.assert_any_call('app2', include_list=None)

    def test_delegate_command_with_one_appconfig_entry(self, run_mutpy_on_app):
        """Check correct delegation to 'run_mutpy_on_app."""
        with self.modify_settings(
                INSTALLED_APPS={"prepend": ['app1.apps.App1Config']}
        ):
            # when
            self.run_command(['app1'])
            # then
            run_mutpy_on_app.assert_called_once_with('app1', include_list=None)


# noinspection PyUnresolvedReferences
@mock.patch('django_mutpy.mutpy_runner.teardown_databases')
@mock.patch('django_mutpy.mutpy_runner.setup_databases')
@mock.patch('django_mutpy.mutpy_runner.teardown_test_environment')
@mock.patch('django_mutpy.mutpy_runner.setup_test_environment')
@mock.patch('django_mutpy.mutpy_runner.build_controller')
@mock.patch('django_mutpy.mutpy_runner.build_parser')
@mock.patch('django_mutpy.mutpy_runner.list_all_modules_in_package',
            return_value=['app1.some_module', 'app1.some_other_module'])
class MutPyRunnerTest(TestCase):
    """Unit tests for the mutpy_runner module."""

    def test_delegation(self, list_all_modules_in_package, build_parser, *_):
        """Check correct delegation to MutPy."""
        # given
        arg_parser = self.mock_build_parser(build_parser)
        # when
        run_mutpy_on_app('app1')
        # then
        list_all_modules_in_package.assert_called_once_with('app1', include_list=None, skip=('migrations', 'tests'))
        arg_parser.parse_args.assert_called_once_with([
            '--target', 'app1.some_module', 'app1.some_other_module',
            '--unit-test', 'app1.tests',
            '--show-mutants',
        ])

    def mock_build_parser(self, build_parser):
        """Mock the build_parser function and make it return a mock parser object."""
        arg_parser = ArgumentParser()
        arg_parser.parse_args = MagicMock(return_value=None)
        build_parser.return_value = arg_parser
        return arg_parser


class UtilsTest(TestCase):
    """Unit tests for utility functions."""

    def test_list_all_modules_in_package(self):
        """Run 'list_all_modules_in_package' against 'test_app' and check result."""
        # when
        all_modules = list_all_modules_in_package('test_app', include_list=None, skip=['tests', 'migrations'])
        # then
        self.assertEqual(all_modules, ['test_app.calculator',
                                       'test_app.models',
                                       'test_app.nested.nested.nested_module',
                                       'test_app.nested.nested_module'])

    def test_with_include_list(self):
        """Run 'list_all_modules_in_package' against 'test_app' and check result."""
        # when
        all_modules = list_all_modules_in_package('test_app',
                                                  include_list=[
                                                      'test_app.models',
                                                      'test_app.nested.nested.nested_module'
                                                  ],
                                                  skip=['tests'])
        # then
        self.assertEqual(all_modules, ['test_app.models',
                                       'test_app.nested.nested.nested_module'])


class DjangoCompat(TestCase):
    """Unit tests for the Django compat module."""

    def test_setup_databases(self):
        """Check if the correct 'setup_databases' is used."""
        from django_mutpy.django_compat import setup_databases
        self.assertTrue(callable(setup_databases))

    def test_teardown_databases(self):
        """Check if the correct 'teardown_databases' is used."""
        from django_mutpy.django_compat import teardown_databases
        self.assertTrue(callable(teardown_databases))


class SystemTest(SimpleTestCase):
    """End-to-end tests."""

    def run_muttest_manage_py_command(self, args):
        """Invoke the 'manage.py muttest...' command with arguments."""
        manage_file = __import__('manage').__file__
        try:
            output = subprocess.check_output([sys.executable, manage_file, 'muttest'] + args)
            exit_code = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            exit_code = e.returncode
        return output.decode('utf-8'), exit_code

    def test_output(self):
        """Check the output when running against the test_app."""
        # when
        output, exit_code = self.run_muttest_manage_py_command(['test_app'])
        # then
        self.assertEqual(exit_code, 0)
        self.assertIn('AOR test_app.calculator', output)
        self.assertIn('all: 3', output)
        self.assertIn('survived: 3', output)

    def test_output_with_modules_param(self):
        """Check the output when running against the test_app."""
        # when
        output, exit_code = self.run_muttest_manage_py_command(
            ['test_app', '--modules', 'test_app.nested.nested.nested_module']
        )
        # then
        self.assertEqual(exit_code, 0)
        self.assertIn('all: 0', output)

    def test_run_with_db_tests(self):
        """Test if the Django database test isolation is properly set up."""
        # when
        output, exit_code = self.run_muttest_manage_py_command(['test_app_db'])
        # then
        self.assertEqual(exit_code, 0)
        self.assertNotIn('[*] Tests failed:', output)
