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
        'kubernetes == 5.0.0',
        'django-setuptest==0.2.1',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    zip_safe=False,
)
