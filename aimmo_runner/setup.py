# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="aimmo_runner",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django==3.2.16",
        "django-forms-bootstrap",
        "django-js-reverse",
        "eventlet",
        "requests",
        "six",
        "hypothesis",
        "psutil",
        "docker<6",
        "kubernetes==23.6.0",
    ],
    zip_safe=False,
)
