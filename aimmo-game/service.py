#!/usr/bin/env python
import logging
import os
import sys

# If we monkey patch during testing then Django fails to create a DB environment
if __name__ == '__main__':
    import eventlet
    eventlet.monkey_patch()

import flask
from flask_socketio import SocketIO, emit

from six.moves import range

from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.location import Location
from simulation.game_state import GameState
from simulation.turn_manager import TURN_MANAGERS
from simulation.worker_manager import WORKER_MANAGERS

app = flask.Flask(__name__)
socketio = SocketIO()

worker_manager = None


def to_cell_type(cell):
    if not cell.is_habitable:
        return 1
    if cell.generates_score:
        return 2
    return 0


def player_dict(avatar):
    # TODO: implement better colour functionality: will eventually fall off end of numbers
    colour = "#%06x" % (avatar.user_id * 4999)
    return {
        'id': avatar.user_id,
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
    with turn_manager.game_state as game_state:
        world = game_state.world_map
        num_cols = world.num_cols
        num_rows = world.num_rows
        grid = [[to_cell_type(world.get_cell(Location(x, y)))
                 for y in range(num_rows)]
                for x in range(num_cols)]
        player_data = {p.user_id: player_dict(p)
                       for p in game_state.avatar_manager.avatars}
        return {
            'players': player_data,
            'score_locations': [(cell.location.x, cell.location.y)
                                for cell in world.score_cells],
            'pickup_locations': [(cell.location.x, cell.location.y)
                                 for cell in world.pickup_cells],
            'map_changed': True,  # TODO: experiment with only sending deltas (not if not required)
            'width': num_cols,
            'height': num_rows,
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
def health_check():
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
    global turn_manager
    global worker_manager

    print("Running game...")
    my_map = map_generator.generate_map(10, 10, 0.1)
    player_manager = AvatarManager()
    game_state = GameState(my_map, player_manager)

    TurnManagerClass = TURN_MANAGERS[os.environ.get('TURN_MANAGER', 'concurrent')]
    turn_manager = TurnManagerClass(
        game_state=game_state,
        end_turn_callback=send_world_update
    )
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
