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
    name='aimmo-game-worker',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ],
    tests_require=[
        'httmock',
        'mock'
    ],
    test_suite='tests',
    zip_safe=False,
)

if withcoverage == 'True':
    print("saving coverage stats")
    cov.save()
    print("exiting program")