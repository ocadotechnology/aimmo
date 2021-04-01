# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="aimmo-game-worker",
    packages=find_packages(),
    version="0.0.0",
    include_package_data=True,
    tests_require=["pytest", "httmock", "mock"],
    setup_requires=["pytest-runner"],
    test_suite="tests",
)
