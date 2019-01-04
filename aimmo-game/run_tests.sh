#!/bin/bash
coverage=$1
function coverage_ready {
    output=$(find .coverage)
    if [ $output = '.coverage' ]; then
        echo '.coverage file found!'
        ls -a
        mv .coverage coveragedata/.coverage
        cd coveragedata
        ls -a
        exit
    fi
}

if [ $coverage = '-c' ]; then
    echo 'Collecting coverage...'
    coverage run setup.py test
    for i in {1..5}; do
        echo 'Waiting for .coverage file...'
        coverage_ready
        sleep 3
    done
else
    python setup.py test
fi
