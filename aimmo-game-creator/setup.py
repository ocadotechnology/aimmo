# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import sys
import os

try:
    with_coverage = os.environ['COVERAGE']
    print('Generating coverage data.')
    if with_coverage:
        import coverage
        cov = coverage.Coverage()
        cov.start()
except:
    print('Not generating coverage data.')

setup(
    name='aimmo-game-creator',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'eventlet',
        'kubernetes >= 6.0.0'
    ],
    tests_require=[
        'httmock',
    ],
    test_suite='tests',
    zip_safe=False,
)

try:
    with_coverage = os.environ['COVERAGE']
    if with_coverage:
        cov.stop()
        cov.save()
except:
    pass
