"""Setup script."""
from os import path

from setuptools import setup, find_packages

from django_mutpy import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-mutpy',
    version='.'.join(str(x) for x in __version__),
    license='Apache 2.0',
    description='Mutation testing with MutPy for Django.',
    long_description=long_description,
    author='Philipp Hossner',
    author_email='philipp.hossner@posteo.de',
    url='https://github.com/phihos/django-mutpy',
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'mutpy>=0.5.1',
        'Django>=1.8'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ]
)
