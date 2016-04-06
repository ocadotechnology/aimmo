#!/usr/bin/env python
import sys

import requests

url = 'http://localhost:5000/initialise/'

if len(sys.argv) > 1:
    avatar_file = sys.argv[1]
else:
    avatar_file = '../players/avatar_examples/dumb_avatar.py'

with open(avatar_file) as avatar_fileobj:
    avatar_data = avatar_fileobj.read()

api_data = {
    'code': avatar_data,
    'options': {},
}

print 'Posting: ', api_data
result = requests.post(url, json=api_data)
print result.content
result.raise_for_status()
