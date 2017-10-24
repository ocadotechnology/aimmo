#!/usr/bin/env python
import cPickle as pickle
import logging
import os
import sys
from collections import defaultdict

import eventlet

eventlet.sleep()
eventlet.monkey_patch()

import flask
from flask_socketio import SocketIO, emit

from simulation.turn_manager import state_provider
from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.turn_manager import ConcurrentTurnManager
from simulation.worker_manager import WORKER_MANAGERS

app = flask.Flask(__name__)
socketio = SocketIO()

worker_manager = None


def to_cell_type(cell):
    if not cell.habitable:
        return 1
    if cell.generates_score:
        return 2
    return 0


def player_dict(avatar):
    # TODO: implement better colour functionality: will eventually fall off end of numbers
    colour = "#%06x" % (avatar.player_id * 4999)
    return {
        'id': avatar.player_id,
        'x': avatar.location.x,
        'y': avatar.location.y,
        'health': avatar.health,
        'score': avatar.score,
        'rotation': 0,
        "colours": {
            "bodyStroke": "#0ff",
            "bodyFill": colour,
            "eyeStroke": "#aff",
            "eyeFill": "#eff",
        }
    }


def get_world_state():
    with state_provider as game_state:
        world = game_state.world_map
        player_data = {p.player_id: player_dict(p) for p in game_state.avatar_manager.avatars}
        grid_dict = defaultdict(dict)
        for cell in world.all_cells():
            grid_dict[cell.location.x][cell.location.y] = to_cell_type(cell)
        pickups = []
        for cell in world.pickup_cells():
            pickup = cell.pickup.serialise()
            pickup['location'] = (cell.location.x, cell.location.y)
            pickups.append(pickup)
        return {
                'players': player_data,
                'score_locations': [(cell.location.x, cell.location.y) for cell in world.score_cells()],
                'pickups': pickups,
                # TODO: experiment with only sending deltas (not if not required)
                'map_changed': True,
                'width': world.num_cols,
                'height': world.num_rows,
                'minX': world.min_x(),
                'minY': world.min_y(),
                'maxX': world.max_x(),
                'maxY': world.max_y(),
                'layout': grid_dict,
            }


@socketio.on('connect')
def world_update_on_connect():
    emit(
        'world-update',
        get_world_state(),
    )


def send_world_update():
    socketio.emit(
        'world-update',
        get_world_state(),
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
    socketio.run(
        app,
        debug=False,
        host=sys.argv[1],
        port=int(sys.argv[2]),
        use_reloader=False,
    )
