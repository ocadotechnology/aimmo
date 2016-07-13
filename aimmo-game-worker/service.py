#!/usr/bin/env python
import logging
import sys
import json

import flask

from simulation.world_map import WorldMap
from simulation.avatar_state import AvatarState

# workaround to avoid filename conflicts - in kubernetes this can just be
# called 'avatar.py'
from importlib import import_module

data_dir = sys.argv[3]
import_module('{}.avatar'.format(data_dir))
from avatar import Avatar

app = flask.Flask(__name__)


@app.route('/turn/', methods=['POST'])
def process_turn():
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    action = avatar.handle_turn(avatar_state, world_map)

    return flask.jsonify(action=action.serialise())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    global avatar
    options = json.loads(open('./{}/options.json'.format(data_dir)))
    avatar = Avatar(**options)

    app.config['DEBUG'] = True
    app.run(
        host=sys.argv[1],
        port=int(sys.argv[2]),
    )
