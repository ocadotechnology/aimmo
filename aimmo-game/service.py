#!/usr/bin/env python
import eventlet

eventlet.sleep()
eventlet.monkey_patch()

import cPickle as pickle
import logging
import os
import sys
import time

import flask
from flask_socketio import SocketIO

from simulation.turn_manager import state_provider
from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.turn_manager import ConcurrentTurnManager
from simulation.worker_manager import WORKER_MANAGERS
from simulation.world_state import WorldState

app = flask.Flask(__name__)
socketio = SocketIO()

class WorldStateManager():
    def __init__(self):
        self.world_states = {}

    def get_world_state(self, player_id):
        return self.world_states[player_id]

    def add_world_state(self, world_state):
        self.world_states[world_state.player_id] = world_state

    def get_all_world_states(self):
        values = []
        for key, value in self.world_states.iteritems():
            values.append(value)
        return values

worker_manager = None
world_state_manager = WorldStateManager()

"""
    The order of events is:
     > server: world_init
     > client: client-ready, id
     > server: broadcast world-update for each state
     > client: filter my updates
"""

@socketio.on('connect')
def world_init():
    socketio.emit('world-init')

@socketio.on('client-ready')
def client_ready(user_id):
    print("Received user id: " + str(user_id))
    world_state_manager.add_world_state(WorldState(state_provider, user_id))
    world_state_manager.get_world_state(user_id).ready_to_update = True

def send_world_update():
    # TODO: For the moment we broadcast all the updates and we filter them in the
    # Unity client. We want to get rid of this.

    for world_state in world_state_manager.get_all_world_states():
        if world_state.ready_to_update:
            socketio.emit(
                'world-update',
                world_state.get_updates(),
                broadcast=True,
            )

@app.route('/')
def healthcheck():
    return 'HEALTHY'

@app.route('/player/<player_id>')
def player_data(player_id):
    player_id = int(player_id)
    return flask.jsonify({
        'code': worker_manager.get_code(player_id),
        'options': {},       # Game options
        'state': None,
    })

def run_game(port):
    global worker_manager

    print("Running game...")
    settings = pickle.loads(os.environ['settings'])

    # TODO: this does not work with Kubernates; locally it works
    # as http://localhost:8000/players/api/games/ is used as default
    api_url = os.environ.get('GAME_API_URL', 'http://localhost:8000/players/api/games/')
    generator = getattr(map_generator, settings['GENERATOR'])(settings)
    player_manager = AvatarManager()
    game_state = generator.get_game_state(player_manager)

    turn_manager = ConcurrentTurnManager(game_state=game_state, end_turn_callback=send_world_update, completion_url=api_url+'complete/')
    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    worker_manager = WorkerManagerClass(game_state=game_state, users_url=api_url, port=port)

    worker_manager.start()
    turn_manager.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    socketio.init_app(app, resource=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))

    run_game(int(sys.argv[2]))

    # run the flusk persistent connection
    socketio.run(
        app,
        debug=False,
        host=sys.argv[1],
        port=int(sys.argv[2]),
        use_reloader=False,
    )
