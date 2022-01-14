# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="aimmo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "eventlet",
        "requests",
        "djangorestframework==3.12.2",
    ],
    tests_require=[],
    test_suite="test_utils.test_suite.DjangoAutoTestSuite",
    zip_safe=False,
)
