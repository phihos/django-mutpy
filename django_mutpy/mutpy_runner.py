"""Contains functions that directly interact with MutPy."""

from django.test.utils import setup_test_environment, teardown_test_environment
from mutpy.commandline import build_controller, build_parser

from django_mutpy.django_compat import teardown_databases, setup_databases
from django_mutpy.utils import list_all_modules_in_package


def run_mutpy_on_app(app, include_list=None, skip=('migrations', 'tests')):
    """Let MutPy run mutations tests on a single Django app."""
    old_config = setup_django_test_env()
    productive_modules = list_all_modules_in_package(app, include_list=include_list, skip=skip)
    unittest_module = app + '.tests'
    run_mutpy(productive_modules, unittest_module)
    teardown_django_test_env(old_config)


def run_mutpy(productive_modules, unittest_module):
    """Run mutpy with a list of modules and a unit test module."""
    parser = build_parser()
    cfg = parser.parse_args(
        ['--target'] + productive_modules
        + [
            '--unit-test', unittest_module,
            '--show-mutants',
        ]
    )
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
