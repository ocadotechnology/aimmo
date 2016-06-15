#!/usr/bin/env python
import logging
import os
import sys

import eventlet
eventlet.monkey_patch()

import flask
from flask.ext.socketio import SocketIO, emit

from six.moves import range

from simulation.turn_manager import world_state_provider
from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.turn_manager import TurnManager
from simulation.worker_manager import LocalWorkerManager

app = flask.Flask(__name__)
socketio = SocketIO()


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
    try:
        world = world_state_provider.lock_and_get_world()
        num_cols = len(world.world_map.grid)
        num_rows = len(world.world_map.grid[0])
        grid = [[None for y in range(num_rows)] for x in range(num_cols)]
        for cell in world.world_map.all_cells():
            grid[cell.location.x][cell.location.y] = to_cell_type(cell)
        player_data = {p.player_id: player_dict(p) for p in world.avatar_manager.avatars}
        return {
                'players': player_data,
                'score_locations': [(cell.location.x, cell.location.y) for cell in world.world_map.score_cells()],
                'pickup_locations': [(cell.location.x, cell.location.y) for cell in world.world_map.pickup_cells()],
                'map_changed': True,  # TODO: experiment with only sending deltas (not if not required)
                'width': num_cols,
                'height': num_rows,
                'layout': grid,
            }
    finally:
        world_state_provider.release_lock()


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


def run_game():
    print("Running game...")
    my_map = map_generator.generate_map(10, 10, 0.1)
    player_manager = AvatarManager()
    game_state = GameState(my_map, player_manager)
    turn_manager = TurnManager(game_state=game_state, end_turn_callback=send_world_update)
    worker_manager = LocalWorkerManager(game_state=game_state, users_url=os.environ.get('GAME_API_URL', 'http://localhost:8000/players/api/games/'))
    worker_manager.start()
    turn_manager.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    socketio.init_app(app, resource=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))
    run_game()
    socketio.run(
        app,
        debug=True,
        host=sys.argv[1],
        port=int(sys.argv[2]),
        use_reloader=False,
    )
