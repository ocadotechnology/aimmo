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
    test_suite='tests',
    zip_safe=False,
)
