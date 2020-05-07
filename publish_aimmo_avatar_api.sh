#!/bin/bash

pushd aimmo-game-worker

# build the package
python setup.py sdist wheel

# upload to PyPi
twine upload dist/* --username ${PYPI_USERNAME} --password ${PYPI_PASSWORD} --non-interactive

popd
