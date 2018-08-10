# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='aimmo-game-worker',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
        'six'
    ],
    tests_require=[
        'httmock',
    ],
    test_suite='tests',
    zip_safe=False,
)
