# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import coverage
import sys
import os


withcoverage = os.environ.get('WITH_COVERAGE')

if withcoverage == 'True':
    print("starting code coverage engine")
    coveragedatafile = ".coverage"
    cov = coverage.Coverage(config_file=False)
    cov.start()


setup(
    name='aimmo-game',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'flask',
        'flask-cors',
        'python-socketio==2.0.0',
        'requests',
        'six',
        'kubernetes'
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        'pytest',
        'pytest-asyncio',
        'asynctest',
        'httmock',
        'mock',
        'hypothesis'
    ],
    test_suite='tests',
    zip_safe=False,
)

if withcoverage == 'True':
    print("saving coverage stats")
    cov.save()
    #os.system("bash -c 'rm -f .coverage ; ln -s %s .coverage'" % (coveragedatafile))
    os.system("bash -c 'coverage report > coverage-report.txt'")
    print("exiting program")