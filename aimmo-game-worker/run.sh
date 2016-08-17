#!/bin/bash
set -e

dir=$(mktemp -d)

./initialise.py $dir

export PYTHONPATH=$dir:$PYTHONPATH

exec ./service.py $1 $2 $dir
