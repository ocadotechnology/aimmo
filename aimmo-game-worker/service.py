#!/usr/bin/env python
import logging
import sys
import os
import json

import flask
import requests

from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap
from avatar_runner import AvatarRunner

app = flask.Flask(__name__)
LOGGER = logging.getLogger(__name__)

avatar_runner = None


def get_code_and_options():
    LOGGER.info('Data url: ' + os.environ['DATA_URL'])
    url = os.environ['DATA_URL']
    return requests.get(url).json()


def write_code_to_file(code):
    with open('avatar.py', 'w') as avatar_file:
        avatar_file.write(code)


def write_options_to_file(options):
    with open('options.json', 'w') as options_file:
        json.dump(options, options_file)


def update_code_and_options():
    data = get_code_and_options()
    LOGGER.info('New code is: ' + data['code'])
    write_code_to_file(data['code'])
    write_options_to_file(data['options'])


@app.route('/turn/', methods=['POST'])
def process_turn():
    update_code_and_options()
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    action, logs = avatar_runner.process_avatar_turn(world_map, avatar_state)

    return flask.jsonify(action=action, logs=logs)


def run(host, port):
    logging.basicConfig(level=logging.DEBUG)
    global avatar_runner
    avatar_runner = AvatarRunner()
    app.config['DEBUG'] = False
    app.run(host, port)


if __name__ == '__main__':
    run(host=sys.argv[1], port=int(sys.argv[2]))
