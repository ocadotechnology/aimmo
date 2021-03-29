#!/bin/sh
cd "$(dirname "$0")"

# build the wheel
cd ../aimmo-game-worker
python setup.py bdist_wheel
cd ..

# Copy wheel to django's static directory
mkdir -p aimmo/static/worker/
cp aimmo-game-worker/dist/*.whl aimmo/static/worker/
