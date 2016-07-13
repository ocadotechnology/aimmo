#!/usr/bin/env python

import os
import sys
import json
import requests

data_dir = sys.argv[1]

url = os.environ['DATA_URL']
data = requests.get(url).json()

options = data['options']
with open('{}/options.json'.format(data_dir), 'w') as options_file:
    json.dump(options, options_file)

code = data['code']
with open('{}/avatar.py'.format(data_dir), 'w') as avatar_file:
    avatar_file.write(code)
