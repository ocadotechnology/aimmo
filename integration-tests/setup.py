from setuptools import find_packages, setup
import unittest
import os

def custom_test_suite():
    """ 
        To run the minikube integration tests set:
            os.environ['RUN_KUBE_TESTS'] = "SET"     
    """
    os.environ['RUN_KUBE_TESTS'] = "SET"
    return unittest.TestLoader().discover('tests', pattern='test_*.py')

setup(
    name='integration-tests',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    tests_require=[
        'httmock'
    ],
    test_suite="setup.custom_test_suite",
    zip_safe=False,
)
