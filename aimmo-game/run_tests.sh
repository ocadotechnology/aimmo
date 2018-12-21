#!/bin/bash
coverage=$1

function coverage_ready {
    if [ -e .coverage ]; then
        exit
    fi
}

if [ $coverage = '-c' ]; then
    echo 'Collecting coverage...'
    coverage run setup.py test
    for i in {1..5}; do
        coverage_ready
        echo 'Waiting for .coverage file...'
        sleep 3
    done
else
    python setup.py test
fi
