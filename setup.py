# -*- coding: utf-8 -*-
import re
import sys

from setuptools import find_packages, setup

with open('aimmo/__init__.py', 'r') as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
        fd.read(),
        re.MULTILINE
    ).group(1)

try:
    from semantic_release import setup_hook

    setup_hook(sys.argv)
except ImportError:
    pass

setup(
    name="aimmo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django >= 1.8.3, <= 1.10.8",
        "django-autoconfig >= 0.3.6, < 1.0.0",
        "django-forms-bootstrap",
        "django-js-reverse",
        "djangorestframework>=3.8.2, < 3.9.0",
        "eventlet",
        "flask",
        "flask-socketio",
        "requests",
        "six",
        "hypothesis",
        "flask-cors >= 3.0, < 3.1",
        "psutil >= 5.4, < 5.5",
        "RestrictedPython == 4.0.b7",
    ],
    tests_require=[
        "httmock",
        "mock == 2.0.0",
        "docker >= 3.5, < 3.6",
        "kubernetes == 5.0.0",
        "PyYAML == 4.2b1",
    ],
    version=version,
    zip_safe=False,
)
