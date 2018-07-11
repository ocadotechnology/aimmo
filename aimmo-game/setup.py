# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='aimmo-game',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'flask',
        'flask-socketio',
        'requests',
        'six',
        'pykube',
    ],
    tests_require=[
        'httmock',
        'mock'
    ],
    test_suite='tests',
    zip_safe=False,
)
