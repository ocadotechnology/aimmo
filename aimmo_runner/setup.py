# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="aimmo_runner",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django >= 1.8.3, < 1.9.0",
        "django-autoconfig >= 0.3.6, < 1.0.0",
        "django-forms-bootstrap",
        "django-js-reverse",
        "eventlet",
        "requests",
        "six",
        "hypothesis",
        "psutil",
        "docker >= 3.5, < 3.6",
        "kubernetes == 10.0.0",
    ],
    zip_safe=False,
)
