#!bin/bash
set -e

dir=$(mktemp -d)

./initialise.py $dir

exec ./service.py $1 $2 $dir