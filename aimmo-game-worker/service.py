#!/usr/bin/env python
import logging
import sys
import flask

from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap
from avatar_runner import AvatarRunner

app = flask.Flask(__name__)
LOGGER = logging.getLogger(__name__)

avatar_runner = None


@app.route('/turn/', methods=['POST'])
def process_turn():
    LOGGER.info('Calculating action')
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])
    avatar_state = AvatarState(**data['avatar_state'])

    action, log = avatar_runner.process_avatar_turn(world_map, avatar_state)

    return flask.jsonify(action=action, log=log)


def run(host, port):
    logging.basicConfig(level=logging.DEBUG)
    global avatar_runner
    avatar_runner = AvatarRunner()
    app.config['DEBUG'] = False
    app.run(host, port)


if __name__ == '__main__':
    run(host=sys.argv[1], port=int(sys.argv[2]))
