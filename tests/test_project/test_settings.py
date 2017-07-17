"""Django settings for the test project."""

import os

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'test_project',
    'test_app',
    'test_app_db',
    'django_mutpy'
]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE_CLASSES = []
