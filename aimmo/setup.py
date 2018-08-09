# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='aimmo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'flask',
        'requests',
        'six',
    ],
    tests_require=[
        'httmock',
        'mock',
    ],
    test_suite='test_utils.test_suite.DjangoAutoTestSuite',
    zip_safe=False,
)
