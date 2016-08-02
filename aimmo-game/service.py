#!/usr/bin/env python
import logging
import os
import sys

import eventlet
eventlet.monkey_patch()

import flask
from flask_socketio import SocketIO, emit

from six.moves import range

from simulation.turn_manager import state_provider
from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.turn_manager import ConcurrentTurnManager
from simulation.turn_manager import SequentialTurnManager
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


def player_dict(avatar, min_x, min_y):
    # TODO: implement better colour functionality: will eventually fall off end of numbers
    colour = "#%06x" % (avatar.player_id * 4999)
    return {
        'id': avatar.player_id,
        'x': avatar.location.x-min_x,
        'y': avatar.location.y-min_y,
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
        grid = [[to_cell_type(cell) for cell in column] for column in world]
        min_x = world.min_x()
        min_y = world.min_y()
        player_data = {p.player_id: player_dict(p, min_x, min_y) for p in game_state.avatar_manager.avatars}
        return {
                'players': player_data,
                'score_locations': [(cell.location.x-min_x, cell.location.y-min_y)
                                    for cell in world.score_cells()],
                'pickup_locations': [(cell.location.x-min_x, cell.location.y-min_y)
                                     for cell in world.pickup_cells()],
                # TODO: experiment with only sending deltas (not if not required)
                'map_changed': True,
                'width': world.num_cols,
                'height': world.num_rows,
                'min_x': min_x,
                'min_y': min_y,
                'layout': grid,
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


def run_game():
    global worker_manager

    print("Running game...")
    my_map = map_generator.generate_map(10, 10, 0.1)
    player_manager = AvatarManager()
    game_state = GameState(my_map, player_manager)
    turn_manager = ConcurrentTurnManager(game_state=game_state, end_turn_callback=send_world_update)
    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    worker_manager = WorkerManagerClass(
        game_state=game_state,
        users_url=os.environ.get('GAME_API_URL', 'http://localhost:8000/players/api/games/')
    )
    worker_manager.start()
    turn_manager.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    socketio.init_app(app, resource=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))
    run_game()
    socketio.run(
        app,
        debug=False,
        host=sys.argv[1],
        port=int(sys.argv[2]),
        use_reloader=False,
    )
