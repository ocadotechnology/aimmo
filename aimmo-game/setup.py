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
        "prometheus_client",
        "docker",
    ],
    setup_requires=["pytest-runner"],
    tests_require=[
        "socketIO-client",
        "pytest==4.1.1",
        "pytest-asyncio==0.10.0",
        "pytest-mock",
        "asynctest",
        "httmock",
        "mock",
        "hypothesis",
        "pytest-aiohttp",
        "aioresponses",
    ],
    test_suite="tests",
    zip_safe=False,
)
