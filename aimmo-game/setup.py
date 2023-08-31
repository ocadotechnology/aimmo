# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup

withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="aimmo-game",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    tests_require=[
        # TODO: These have been left here so the tests can run but they're already defined in Pipfile
        "pytest~=6.2",
        "pytest-mock",
        "pytest-asyncio==0.14.0",  # downgraded because of this issue: https://github.com/pytest-dev/pytest-asyncio/issues/209
        "httmock",
        "asynctest",
        "hypothesis",
        "mock",
        "pytest-aiohttp==0.3.0",
        "aioresponses",
    ],
    setup_requires=["pytest-runner"],
    test_suite="tests",
    zip_safe=False,
)
