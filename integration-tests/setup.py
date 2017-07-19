from setuptools import find_packages, setup
import unittest

def custom_test_suite():
    test_loader = unittest.TestLoader()

    test_suite = test_loader.discover('tests', pattern='test_*.py')
    ktest_suite = test_loader.discover('tests', pattern='ktest_*.py')

    # kubernates tests are not yet fully supported
    all_tests = unittest.TestSuite([test_suite])

    return all_tests

setup(
    name='integration-tests',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    tests_require=[
        'httmock',
    ],
    test_suite="setup.custom_test_suite",
    zip_safe=False,
)
