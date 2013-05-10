#!/usr/bin/env python

from distutils.core import setup

long_description = '''
Use this package to render your forms as JSON objects.

Documentation on https://github.com/rafaelsierra/django-json-mixin-form
''' 

setup(name='sierra-django-json-mixin-form',
      version='1.0',
      description='Utility to render Form responses in a JSON usable format',
      long_description=long_description,
      author='Rafael Sierra',
      author_email='sierra@rafaelsdm.com	',
      url='http://github.com/rafaelsierra/django-json-mixin-form',
      packages=[
                'sierra',
                'sierra.dj',
                'sierra.dj.mixins',
                ],
      package_dir = {'':'src'},
      requires = ['django (>=1.4)'],
      license = 'MIT',
)
