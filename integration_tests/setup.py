# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='integration-tests',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ],
    tests_require=[
        'requests',
        'psutil',
        'mock',
        'kubernetes == 5.0.0',
    ],
    test_suite='test_utils.test_suite.DjangoAutoTestSuite',
    zip_safe=False,
)
