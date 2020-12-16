# -*- coding: utf-8 -*-
import re
import sys

from setuptools import find_packages, setup

with open("aimmo/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name="aimmo",
    packages=find_packages(exclude=["*.tests", "*.tests.*"]),
    package_dir={"aimmo": "aimmo"},
    include_package_data=True,
    install_requires=[
        "django==2.2.17",
        "django-js-reverse==0.9.1",
        "djangorestframework==3.12.2",
        "eventlet==0.29.1",
        "requests==2.25.0",
        "hypothesis==5.41.3",
        "cfl-common",
    ],
    tests_require=["docker >= 3.5, < 3.6", "kubernetes == 5.0.0", "PyYAML == 4.2b1"],
    version=version,
    zip_safe=False,
)
