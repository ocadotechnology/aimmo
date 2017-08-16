#!/usr/bin/env python

import os
import sys
import yaml

try:
    os.makedirs(os.path.join(sys.argv[1], 'manifests'))
except OSError:
    pass

for filename in os.listdir(os.path.join(sys.argv[1], 'manifests-template')):
    content = open(os.path.join(sys.argv[1], 'manifests-template', filename)).read()
    content = content.replace('AIMMO_VERSION', sys.argv[2])
    content = content.replace('AIMMO_UI_URL', sys.argv[3])
    dest_filename = os.path.join(sys.argv[1], 'manifests', filename)
    with open(dest_filename, 'w') as fobj:
        fobj.write(content)
