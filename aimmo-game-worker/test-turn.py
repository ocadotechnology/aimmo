#!/usr/bin/env python
import requests

url = 'http://localhost:5000/turn/'

api_data = {
    'world_map': {
        'cells': {
            '0,0': {}
        },
    },
}

print 'Posting:', api_data
result = requests.post(url, json=api_data)
print result.content
result.raise_for_status()
print 'Output:', result.json()
