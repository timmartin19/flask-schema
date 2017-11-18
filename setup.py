#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'jsonschema',
    'flask'
]

test_requirements = [
    'pylint',
    'unittest2',
    'webtest'
    # TODO: put package test requirements here
]

setup(
    name='flask-schema',
    version='0.1.0',
    description="Use JSON Schema to validate incoming requests",
    long_description=readme + '\n\n' + history,
    author="Tim Martin",
    author_email='oss@timmartin.me',
    url='https://github.com/timmartin19/flask-schema',
    py_modules=['flask_schema'],
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='flask_schema',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='flask_schema_tests',
    tests_require=test_requirements
)
