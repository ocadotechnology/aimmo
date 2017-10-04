#!/usr/bin/env python
import requests
from logging import getLogger

LOGGER = getLogger(__name__)

url = 'http://localhost:5001/turn/'

avatar = {'location': {'x': 0, 'y': 0}, 'health': 5, 'score': 0, 'events': []}
api_data = {
    'avatar_state': avatar,
    'world_map': {
        'cells': [
            {'location': {'x': 0, 'y': 0}, 'habitable': True, 'avatar': avatar, 'pickup': None},
            {'location': {'x': 1, 'y': 0}, 'habitable': False, 'avatar': None, 'pickup': None},
            {'location': {'x': -1, 'y': 0}, 'habitable': True, 'avatar': avatar, 'pickup': {'health_restored': 3}},
        ],
    }
}

LOGGER.debug("Posting:", api_data)
result = requests.post(url, json=api_data)
result.raise_for_status()
LOGGER.debug("Output:", result.json())
