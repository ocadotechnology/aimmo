from setuptools import setup
import unittest


def custom_test_suite():
    return unittest.TestLoader().discover('tests', pattern='test_*.py')


setup(
    name='integration-tests',
    include_package_data=True,
    install_requires=[
    ],
    tests_require=[
        'httmock',
        'psutil'
    ],
    test_suite="setup.custom_test_suite",
    zip_safe=False,
)
