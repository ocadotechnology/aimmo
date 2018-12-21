# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import sys
import os


withcoverage = os.environ.get('WITH_COVERAGE')

setup(
    name='aimmo-game',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'flask',
        'flask-cors',
        'python-socketio==2.0.0',
        'requests',
        'six',
        'kubernetes'
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio',
        'asynctest',
        'httmock',
        'mock',
        'hypothesis'
    ],
    test_suite='tests',
    zip_safe=False,
)
