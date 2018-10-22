#!/usr/bin/env python
import logging
import sys

import flask
import requests

from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap
from avatar_runner import AvatarRunner

app = flask.Flask(__name__)
LOGGER = logging.getLogger(__name__)

avatar_runner = None
DATA_URL = ''


def get_code_and_options():
    data = requests.get(DATA_URL).json()
    return data['code'], data['options']


@app.route('/turn/', methods=['POST'])
def process_turn():
    code, options = get_code_and_options()
    data = flask.request.get_json()
    world_map = WorldMap(**data['world_map'])

    avatar_state = AvatarState(location=data['avatar_state']['location'],
                               score=data['avatar_state']['score'],
                               health=data['avatar_state']['health'])

    response = avatar_runner.process_avatar_turn(world_map, avatar_state, code)

    return flask.jsonify(**response)


def run(host, port, data_url):
    global avatar_runner, DATA_URL
    DATA_URL = data_url
    logging.basicConfig(level=logging.DEBUG)
    avatar_runner = AvatarRunner()
    app.config['DEBUG'] = False
    app.run(host, port)


if __name__ == '__main__':
    run(host=sys.argv[1], port=int(sys.argv[2]), data_url=sys.argv[3])
