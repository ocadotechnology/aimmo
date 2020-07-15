# -*- coding: utf-8 -*-
import os

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
        "python-socketio==4.6.0",
        "requests",
        "six",
        "kubernetes",
        "prometheus_client",
        "docker",
    ],
    tests_require=[
        "pytest",
        "pytest-mock",
        "pytest-asyncio",
        "httmock",
        "asynctest",
        "hypothesis",
        "mock",
        "pytest-aiohttp",
        "aioresponses",
    ],
    setup_requires=["pytest-runner"],
    test_suite="tests",
    zip_safe=False,
)
