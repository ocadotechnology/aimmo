# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import importlib.util

version_spec = importlib.util.spec_from_file_location(
    "aimmo_version", "../aimmo/__init__.py"
)
aimmo_version_module = importlib.util.module_from_spec(version_spec)
version_spec.loader.exec_module(aimmo_version_module)


setup(
    name="aimmo-avatar-api",
    packages=find_packages("simulation"),
    version=aimmo_version_module.__version__,
    include_package_data=True,
    tests_require=["httmock", "mock"],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
