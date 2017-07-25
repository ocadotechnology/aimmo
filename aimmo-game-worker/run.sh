#!/bin/bash

#TODO: no longer needed?

set -e

dir=$(mktemp -d)

python ./initialise.py $dir

export PYTHONPATH=$dir:$PYTHONPATH

exec python ./service.py $1 $2 $dir
