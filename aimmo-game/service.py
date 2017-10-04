#!/usr/bin/env python
import logging
import os
import sys
from json import loads

import eventlet

eventlet.sleep()
eventlet.monkey_patch()

import flask
from flask_socketio import SocketIO

from simulation.managers.turn_manager import state_provider
from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.managers.turn_manager import ConcurrentTurnManager
from simulation.managers.worker_manager import WORKER_MANAGERS
from simulation.state.world_state import WorldState

app = flask.Flask(__name__)
socketio = SocketIO()

worker_manager = None

# Every user has its own world state.
world_state_manager = {}

# socketio routes
@socketio.on('connect')
def world_init():
    socketio.emit('world-init')

@socketio.on('client-ready')
def client_ready(client_id):
    flask.session['id'] = client_id
    world_state = WorldState(state_provider)
    world_state_manager[client_id] = world_state

@socketio.on('exit-game')
def exit_game(user_id):
    del world_state_manager[user_id]

def send_world_update():
    for world_state in world_state_manager.values():
        socketio.emit(
            'world-update',
            world_state.get_updates(),
            broadcast=True,
        )

@socketio.on('disconnect')
def on_disconnect():
    del world_state_manager[flask.session['id']]

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

# Plain client routes... These are easy to work with and
# they are not exposed in the kubernetes application
# as the proxy does not allow communication with them.
@app.route('/plain/<user_id>/connect')
def plain_world_init(user_id):
    world_init()
    return 'CONNECT'

@app.route('/plain/<user_id>/client-ready')
def plain_client_ready(user_id):
    world_state = WorldState(state_provider)
    world_state_manager[int(user_id)] = world_state
    return 'RECEIVED USER READY ' + user_id

@app.route('/plain/<user_id>/exit-game')
def plain_exit_game(user_id):
    return "EXITING GAME FOR USER " + user_id

@app.route('/plain/<user_id>/update')
def plain_update(user_id):
    world_state =  world_state_manager[int(user_id)]
    return flask.jsonify(world_state.get_updates())

def run_game(port):
    global worker_manager

    print("Running game...")
    settings = loads(os.environ['settings'])

    api_url = os.environ['GAME_API_URL']
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

    socketio.run(
        app,
        debug=False,
        host=sys.argv[1],
        port=int(sys.argv[2]),
        use_reloader=False,
    )
