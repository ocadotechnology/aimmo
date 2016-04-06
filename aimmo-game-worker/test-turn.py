#!/usr/bin/env python
import requests
import sys

url = 'http://localhost:5001/turn/'

api_data = {
    'world_map': {
        'cells': {
            '0,0': {}
        },
    },
}

print 'Posting:', api_data
result = requests.post(url, json=api_data)
result.raise_for_status()
print 'Output:', result.json()
