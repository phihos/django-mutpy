"""Contains functions that directly interact with MutPy."""

from django_mutpy.utils import list_all_modules_in_package
from mutpy.commandline import build_controller, build_parser


def run_mutpy_on_app(app, skip=('migrations', 'tests')):
    """Let MutPy run mutations tests on a single Django app."""
    productive_modules = list_all_modules_in_package(app, skip=skip)
    unittest_module = app + '.tests'
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
