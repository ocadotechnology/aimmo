#!/usr/bin/env python
import requests

url = 'http://localhost:5001/turn/'

avatar = {'location': {'x': 0, 'y': 0}, 'health': 5, 'score': 0, 'events': []}
api_data = {
    'avatar_state': avatar,
    'world_map': {
        'cells': [
            {'location': {'x': 0, 'y': 0}, 'habitable': True, 'generates_score': True, 'avatar': avatar, 'pickup': None},
            {'location': {'x': 1, 'y': 0}, 'habitable': False, 'generates_score': False, 'avatar': None, 'pickup': None},
            {'location': {'x': -1, 'y': 0}, 'habitable': True, 'generates_score': False, 'avatar': avatar, 'pickup': {'health_restored': 3}},
        ],
    }
}

print 'Posting:', api_data
result = requests.post(url, json=api_data)
result.raise_for_status()
print 'Output:', result.json()
