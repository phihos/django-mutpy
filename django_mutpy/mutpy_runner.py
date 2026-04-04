"""Contains functions that directly interact with MutPy."""

import importlib
import importlib.util

# mutpy uses importlib.find_loader which was removed in Python 3.12.
# Provide a shim so that mutpy.test_runners can be imported on modern Pythons.
if not hasattr(importlib, 'find_loader'):
    def _find_loader_shim(name, path=None):
        try:
            return importlib.util.find_spec(name, path)
        except (ModuleNotFoundError, ValueError):
            return None
    importlib.find_loader = _find_loader_shim

from django.test.utils import (setup_databases, setup_test_environment,
                               teardown_databases, teardown_test_environment)
from mutpy.commandline import build_controller, build_parser

from django_mutpy.utils import list_all_modules_in_package


def run_mutpy_on_app(app, include_list=None, skip=('migrations', 'tests'), extra_args=None):
    """Let MutPy run mutations tests on a single Django app."""
    old_config = setup_django_test_env()
    productive_modules = list_all_modules_in_package(app, include_list=include_list, skip=skip)
    unittest_module = app + '.tests'
    run_mutpy(productive_modules, unittest_module, extra_args=extra_args)
    teardown_django_test_env(old_config)


def run_mutpy(productive_modules, unittest_module, extra_args=None):
    """Run mutpy with a list of modules and a unit test module."""
    parser = build_parser()
    args = (
        ['--target'] + productive_modules
        + [
            '--unit-test', unittest_module,
            '--show-mutants',
        ]
        + (extra_args or [])
    )
    cfg = parser.parse_args(args)
    mutpy_controller = build_controller(cfg)
    mutpy_controller.run()


def teardown_django_test_env(old_config):
    """Tear down the Django test environment and restore the old database configuration."""
    teardown_databases(old_config, 1)
    teardown_test_environment()


def setup_django_test_env():
    """Set up the Django test environment and return the previous database configuration."""
    setup_test_environment()
    old_config = setup_databases(1, True)
    return old_config
