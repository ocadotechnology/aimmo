# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='aimmo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'flask',
        'python-socketio==2.0.0',
        'requests',
        'six',
        'pykube',
    ],
    tests_require=[
        'httmock',
        'mock',
        'django-setuptest==0.2.1',

    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    zip_safe=False,
)
