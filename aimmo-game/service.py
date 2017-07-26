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

def __world_init():
    socketio.emit('world-init')

def __client_ready(user_id):
    print("Received user id: " + str(user_id))
    world_state_manager.add_world_state(WorldState(state_provider, user_id))
    world_state_manager.get_world_state(user_id).ready_to_update = True

def __exit_game(user_id):
    world_state_manager.get_world_state(user_id).ready_to_update = False
    #player_manager.remove_avatar(user_id)

    # If avatar is in there, mark the view as empty.
    user_avatar = player_manager.get_avatar(user_id)
    if not user_avatar is None:
        user_avatar.view.is_empty = True

def __send_world_update():
    for world_state in world_state_manager.get_all_world_states():
        if world_state.ready_to_update:
            socketio.emit(
                'world-update',
                world_state.get_updates(),
                broadcast=True,
            )

# plain client routes
@app.route('/plain/connect')
def plain_world_init():
    __world_init()
    return 'CONNECT'
@app.route('/plain/client-ready/<user_id>')
def plain_client_ready(user_id):
    user_id = int(user_id)
    __client_ready(user_id)
    return 'RECEIVED USER READY ' + str(user_id)
@app.route('/plain/exit-game/<user_id>')
def plain_exit_game(user_id):
    user_id = int(user_id)
    __exit_game(user_id)
    return "EXITING GAME FOR USER " + str(user_id)
@app.route('/plain/server-ready/<user_id>')
def plain_ready(user_id):
    user_id = int(user_id)
    world_state = world_state_manager.get_world_state(user_id)
    if not world_state.ready_to_update:
        return "NOT READY"
    else:
        return "READY"
@app.route('/plain/update/<user_id>')
def plain_update(user_id):
    user_id = int(user_id)
    world_state = world_state_manager.get_world_state(user_id)
    if not world_state.ready_to_update:
        return "NOT READY"
    return  flask.jsonify(world_state.get_updates())

# socketio routes
@socketio.on('connect')
def world_init(): __world_init()
@socketio.on('client-ready')
def client_ready(user_id): __client_ready(user_id)
@socketio.on('exit-game')
def exit_game(user_id): __exit_game(user_id)
def send_world_update(): __send_world_update()

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

    global player_manager
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
