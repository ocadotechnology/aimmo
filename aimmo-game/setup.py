# -*- coding: utf-8 -*-
import os

from setuptools import find_packages, setup

withcoverage = os.environ.get("WITH_COVERAGE")

setup(
    name="aimmo-game",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "aiohttp==3.7.4",
        "aiohttp-cors",
        "aiohttp-wsgi",
        "eventlet==0.31.0",
        "kubernetes==21.7.0",
        "python-socketio==5.0.3",
        "docker==4.4.4",
        "google-api-python-client==1.12.8",
        "google-cloud-logging==2.2.0",
        "grpcio==1.43.0",
    ],
    tests_require=[
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
