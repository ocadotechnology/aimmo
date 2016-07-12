#!/usr/bin/env python
import logging
import sys

import flask

from simulation.world_map import WorldMap
from simulation.avatar_state import AvatarState

app = flask.Flask(__name__)

avatar = None


@app.route('/initialise/', methods=['POST'])
def initialise():
    global avatar

    if avatar:
        flask.abort(400, 'Unable to initialise Avatar service more than once.')

    data = flask.request.get_json()

    try:
        exec(data['code'])
        avatar = Avatar(**data['options'])
    except Exception as e:
        return flask.jsonify(result='code_error', details=str(e))
    else:
        return flask.jsonify(result='success')


@app.route('/turn/', methods=['POST'])
def process_turn():
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    action = avatar.handle_turn(avatar_state, world_map)

    return flask.jsonify(action=action.serialise())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app.config['DEBUG'] = True
    app.run(
        host=sys.argv[1],
        port=int(sys.argv[2]),
    )
