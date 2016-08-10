#!/usr/bin/env python
import logging
import os
import sys
import json

import flask

from simulation.world_map import WorldMap
from simulation.avatar_state import AvatarState

from avatar import Avatar

app = flask.Flask(__name__)


@app.route('/turn/', methods=['POST'])
def process_turn():
    app.logger.info('Processing turn')
    if flask.request.args.get('auth_token') != os.environ['AUTH_TOKEN']:
        app.logger.warning('Invalid auth token %s, expected %s', flask.request.args.get('auth_token'), os.environ['AUTH_TOKEN'])
        flask.abort(403)
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    action = avatar.handle_turn(avatar_state, world_map)

    return flask.jsonify(action=action.serialise())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    global avatar
    with open('{}/options.json'.format(sys.argv[3])) as option_file:
        options = json.load(option_file)
    avatar = Avatar(**options)

    app.config['DEBUG'] = False
    app.run(
        host=sys.argv[1],
        port=int(sys.argv[2]),
    )
