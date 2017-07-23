"""Contains the 'manage.py muttest' command."""

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from django_mutpy.mutpy_runner import run_mutpy_on_app


def check_apps(apps):
    """Check if a list of apps is entirely contained in the list of installed apps."""
    for app in apps:
        installed_apps = settings.INSTALLED_APPS
        if app not in installed_apps:
            raise CommandError('App %s not contained in INSTALLED_APPS %s'
                               % (app, settings.INSTALLED_APPS))


class Command(BaseCommand):
    """This command runs MutPy agains one or more Django apps."""

    can_import_settings = True

    def add_arguments(self, parser):
        """Define cmd arguments."""
        parser.add_argument('app', nargs='+', type=str)
        parser.add_argument('--modules', nargs='+', type=str, default=None)

    def handle(self, *args, **options):
        """Run MutPy against the provided apps."""
        check_apps(options['app'])
        for app in options['app']:
            run_mutpy_on_app(app, include_list=options['modules'])
