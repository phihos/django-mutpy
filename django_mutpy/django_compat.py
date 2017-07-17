from distutils.version import StrictVersion

import django


def teardown_databases108(old_config, verbosity, keepdb=False):
    """
    Destroys all the non-mirror databases.
    """
    old_names, mirrors = old_config
    for connection, old_name, destroy in old_names:
        if destroy:
            connection.creation.destroy_test_db(old_name, verbosity, keepdb)


def teardown_databases109(old_config, verbosity, parallel=0, keepdb=False):
    """
    Destroy all the non-mirror databases.
    """
    for connection, old_name, destroy in old_config:
        if destroy:
            if parallel > 1:
                for index in range(parallel):
                    connection.creation.destroy_test_db(
                        number=index + 1,
                        verbosity=verbosity,
                        keepdb=keepdb,
                    )
            connection.creation.destroy_test_db(old_name, verbosity, keepdb)


DJANGO_VERSION = StrictVersion(django.__version__)

if DJANGO_VERSION < StrictVersion('1.11.0'):
    from django.test.runner import setup_databases
else:
    from django.test.utils import setup_databases
setup_databases = setup_databases

if DJANGO_VERSION < StrictVersion('1.9.0'):
    teardown_databases = teardown_databases108
elif DJANGO_VERSION < StrictVersion('1.11.0'):
    teardown_databases = teardown_databases109
else:
    from django.test.utils import teardown_databases

    teardown_databases = teardown_databases
