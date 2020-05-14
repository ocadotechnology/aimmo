# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import importlib.util


def get_version():
    try:
        version_spec = importlib.util.spec_from_file_location(
            "aimmo_version", "../aimmo/__init__.py"
        )
        aimmo_version_module = importlib.util.module_from_spec(version_spec)
        version_spec.loader.exec_module(aimmo_version_module)
        return aimmo_version_module.__version__
    except Exception:
        return "0.0.0"


setup(
    name="aimmo-avatar-api",
    packages=find_packages(include=["simulation"]),
    version=get_version(),
    include_package_data=True,
    tests_require=["httmock", "mock"],
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
