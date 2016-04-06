#!/usr/bin/env python
import logging
import sys

from simulation.world_map import WorldMap

import flask
app = flask.Flask(__name__)

avatar = None


@app.route('/initialise/', methods=['POST'])
def initialise():
    global avatar

    if avatar:
        raise NotImplementedError

    data = flask.request.get_json()

    exec(data['code'])

    avatar = Avatar(**data['options'])

    return flask.jsonify(**{
        'result': 'success',
    })


@app.route('/turn/', methods=['POST'])
def process_turn():
    data = flask.request.get_json()

    world_map = WorldMap(**data['world_map'])

    action = avatar.handle_turn(world_map, events=[])

    return flask.jsonify(**{
        'action': action.serialise(),
    })



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    app.config['DEBUG'] = True
    app.run(port=int(sys.argv[1]))
