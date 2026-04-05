django-mutpy
============

|Build Status|

Django integration for the mutation testing framework `MutPy`_.

MutPy is a mutation test framework for Python. It basically seeds a bug
into your code and then runs your unit tests to see if they find it.
Mutation testing helps to identify flaws in your tests. Because if your
tests can not uncover obvious bugs, they will also not uncover complex
ones.

This Django app eases the integration of MutPy into your Django project.
It takes care of setting up the Django environment for the tests and
finding the unit tests and the production code.

Requirements
------------

-  Python >= 3.9
-  Django 4.2, 5.0, 5.1, or 5.2
-  MutPy >= 0.5.1

Installation
------------

First install the module.

Either

::

    pip install django-mutpy

or download the repository and

::

    git clone https://github.com/phihos/django-mutpy.git
    cd django-mutpy
    python setup.py install

Then add django\_mutpy to the list of installed apps.

.. code:: python

    INSTALLED_APPS = [
      ...
      'django_mutpy',
      ...
      ]

AppConfig dotted paths (e.g. ``'myapp.apps.MyAppConfig'``) in
``INSTALLED_APPS`` are also supported.

Usage
-----

Run

::

    python manage.py muttest <app1> <app2> ... [--modules <list of modules to include>]
        [--mutpy-args "<extra mutpy flags>"]

Use ``--modules`` to limit mutation testing to specific modules within an app.

Use ``--mutpy-args`` to pass additional flags directly to MutPy as a single
quoted string, for example::

    python manage.py muttest myapp --mutpy-args="--report-html /tmp/report --coverage"

.. _MutPy: https://github.com/mutpy/mutpy
.. |Build Status| image:: https://github.com/phihos/django-mutpy/actions/workflows/test.yml/badge.svg
   :target: https://github.com/phihos/django-mutpy/actions/workflows/test.yml