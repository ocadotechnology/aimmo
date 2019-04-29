# -*- coding: utf-8 -*-
import os
import sys

from setuptools import find_packages, setup

withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="aimmo-game",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "aiohttp-cors",
        "aiohttp-wsgi",
        "eventlet",
        "python-socketio==4.0.0",
        "requests",
        "six",
        "kubernetes",
    ],
    setup_requires=["pytest-runner"],
    tests_require=[
        "pytest==4.0.2",
        "pytest-asyncio",
        "asynctest",
        "httmock",
        "mock",
        "hypothesis",
        "docker",
        "aiohttp",
        "aiohttp_cors",
    ],
    test_suite="tests",
    zip_safe=False,
)
