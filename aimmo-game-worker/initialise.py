#!/usr/bin/env python

import os
import sys
import json
import requests
import logging


LOGGER = logging.getLogger(__name__)


def main(args, url):
    data_dir = args[1]
    LOGGER.debug('Data dir is %s', data_dir)

    data = requests.get(url).json()

    options = data['options']
    with open('{}/options.json'.format(data_dir), 'w') as options_file:
        json.dump(options, options_file)

    code = data['code']
    with open('{}/avatar.py'.format(data_dir), 'w') as avatar_file:
        avatar_file.write(code)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main(sys.argv, url=os.environ['DATA_URL'])
