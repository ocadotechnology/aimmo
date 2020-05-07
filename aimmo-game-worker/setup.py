# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import sys
import os


withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="aimmo-avatar-api",
    packages=find_packages("simulation"),
    include_package_data=True,
    tests_require=["httmock", "mock"],
    test_suite="tests",
    zip_safe=False,
)
