#!/usr/bin/env python
import json
import logging
import sys

import flask

from simulation.avatar_state import AvatarState
from simulation.world_map import WorldMap
from simulation.action import WaitAction

app = flask.Flask(__name__)
LOGGER = logging.getLogger(__name__)

worker_avatar = None


@app.route('/turn/', methods=['POST'])
def process_turn():
    LOGGER.info('Calculating action')
    data = flask.request.get_json()

    try:
        from avatar import Avatar
        global worker_avatar
        worker_avatar = Avatar()

        world_map = WorldMap(**data['world_map'])
        avatar_state = AvatarState(**data['avatar_state'])

        action = worker_avatar.handle_turn(avatar_state, world_map)
    except Exception as e:
        LOGGER.info("Do stuff later with the errored code.")
        LOGGER.info(e)
        action = WaitAction()

    return flask.jsonify(action=action.serialise())


def run(host, port):
    logging.basicConfig(level=logging.DEBUG)

    app.config['DEBUG'] = False
    app.run(host, port)


if __name__ == '__main__':
    run(host=sys.argv[1], port=int(sys.argv[2]))
