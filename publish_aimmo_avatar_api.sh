#!/bin/bash

pushd aimmo-game-worker

# build the package
python setup.py sdist bdist_wheel

# upload to PyPi
twine upload --username ${PYPI_USERNAME} --password ${PYPI_PASSWORD} dist/*

popd
