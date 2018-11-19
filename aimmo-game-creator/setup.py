# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import coverage
import sys
import os


withcoverage = '-c' in sys.argv or '--coverage' in sys.argv

if withcoverage:
    print("starting code coverage engine")
    coveragedatafile = ".coverage"
    cov = coverage.Coverage(config_file=False)
    cov.start()


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

if withcoverage:
    print("saving coverage stats")
    cov.save()
    os.system("bash -c 'rm -f .coverage ; ln -s %s .coverage" % (coveragedatafile))
    os.system("bash -c 'coverage report > coverage-report.txt'")
    print("exiting program")