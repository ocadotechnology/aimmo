# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import sys
import os


withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="aimmo-game-creator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["eventlet"],
    tests_require=["httmock"],
    test_suite="tests",
    zip_safe=False,
)
