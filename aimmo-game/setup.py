# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='aimmo-game',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'flask',
        'python-socketio==2.0.0',
        'requests',
        'six',
        'kubernetes'
    ],
    tests_require=[
        'httmock',
        'mock'
    ],
    test_suite='tests',
    zip_safe=False,
)
