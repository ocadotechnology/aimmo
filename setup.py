# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import versioneer

setup(
    name='aimmo',
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django >= 1.8.3, < 1.9.0',
        'django-autoconfig >= 0.3.6, < 1.0.0',
        'django-js-reverse',
        'eventlet',
        'flask',
        'flask-socketio',
        'requests',
        'six',
        'pykube',
    ],
    tests_require=[
        'django-setuptest',
        'httmock',
    ],
    test_suite='setuptest.setuptest.SetupTestSuite',
    version=versioneer.get_version(),
    zip_safe=False,
)
