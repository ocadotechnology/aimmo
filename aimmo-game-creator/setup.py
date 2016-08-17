# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='aimmo-game-creator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pykube',
    ],
    tests_require=[
    ],
    test_suite='tests',
    zip_safe=False,
)
