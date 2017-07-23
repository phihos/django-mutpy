# django-mutpy
[![Build Status](https://travis-ci.org/phihos/django-mutpy.svg?branch=master)](https://travis-ci.org/phihos/django-mutpy)
[![Coverage Status](https://coveralls.io/repos/github/phihos/django-mutpy/badge.svg?branch=master)](https://coveralls.io/github/phihos/django-mutpy?branch=master)
[![Code Climate](https://codeclimate.com/github/phihos/django-mutpy/badges/gpa.svg)](https://codeclimate.com/github/phihos/django-mutpy)

Django integration for the mutation testing framework MutPy.

MutPy is a mutation test framework for Python. It basically seeds a bug into your code and then runs your unit tests to see if they find it.
Mutation testing helps to identify flaws in your tests. Because if your tests can not uncover obvious bugs, they will also not uncover complex ones.

This Django app eases the integration of MutPy into your Django project. It takes care of setting up the Django environment for the tests and finding the unit tests and the production code.

## Requirements

  * Python >= 3.3
  * MutPy >= 0.4.1 (currently installed from git)

## Installation

First install the module.
```
git clone https://github.com/phihos/django-mutpy.git
cd django-mutpy
python setup.py install
```
Then add django_mutpy to the list of installed apps.

``` python
INSTALLED_APPS = [
  ...
  'django_mutpy',
  ...
  ]
```

## Usage

Run

```
python manage.py muttest <app1> <app2> ... [--modules <list of modules to include>]
```
