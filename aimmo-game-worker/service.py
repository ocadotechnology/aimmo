#!/usr/bin/env python
import json
import logging
import sys

import flask

from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap

app = flask.Flask(__name__)
LOGGER = logging.getLogger(__name__)

worker_avatar = None


@app.route('/turn/', methods=['POST'])
def process_turn():
    LOGGER.info('Calculating action')
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    action = worker_avatar.handle_turn(avatar_state, world_map)

    return flask.jsonify(action=action.serialise())


def run(host, port, directory):
    logging.basicConfig(level=logging.DEBUG)

    with open('{}/options.json'.format(directory)) as option_file:
        options = json.load(option_file)
    from avatar import Avatar
    global worker_avatar
    worker_avatar = Avatar(**options)

    app.config['DEBUG'] = False
    app.run(host, port)

if __name__ == '__main__':
    run(host=sys.argv[1], port=int(sys.argv[2]), directory=sys.argv[3])
