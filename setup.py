#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

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
      requires = ['django (>=1.4)']
)
