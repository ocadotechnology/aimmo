#!/usr/bin/env python
import os
import logging
import sys
import json
import traceback
from contextlib import contextmanager

import flask
from flask_socketio import SocketIO

from simulation.world_map import WorldMap
from simulation.avatar_state import AvatarState

from logger import SocketLogger
from avatar import Avatar

app = flask.Flask(__name__)
socketio = SocketIO()
logger = SocketLogger(socketio)


@contextmanager
def capture_output(new_stdout):
    old_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield
    except Exception:
        print(traceback.format_exc())
    finally:
        sys.stdout = old_stdout


@app.route('/turn/', methods=['POST'])
def process_turn():
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    with capture_output(logger):
        action = avatar.handle_turn(avatar_state, world_map)

    return flask.jsonify(action=action.serialise())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    global avatar
    with open('{}/options.json'.format(sys.argv[3])) as option_file:
        options = json.load(option_file)
    avatar = Avatar(**options)

    socketio.init_app(app, resource=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))
    socketio.run(
        app,
        debug=False,
        host=sys.argv[1],
        port=int(sys.argv[2]),
    )
