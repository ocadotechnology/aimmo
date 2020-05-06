# -*- coding: utf-8 -*-
from setuptools import find_namespace_packages, setup
import sys
import os


withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="avatar_api",
    packages=find_namespace_packages(include=["avatar_api.*"]),
    # package_dir={"": "simulation"},
    include_package_data=True,
    tests_require=["httmock", "mock"],
    test_suite="tests",
    zip_safe=False,
)
