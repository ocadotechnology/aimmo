from setuptools import find_packages, setup

setup(
    name='integration-tests',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    tests_require=[
        'httmock',
    ],
    zip_safe=False,
)

import os
import subprocess

p = subprocess.Popen(['python', "integration_test.py"], cwd="./tests")
p.communicate()
