#!/usr/bin/env python
import cPickle as pickle
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
from simulation.location import Location
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
        num_cols = world.num_cols
        num_rows = world.num_rows
        grid = [[to_cell_type(world.get_cell(Location(x, y)))
                 for y in range(num_rows)]
                for x in range(num_cols)]
        player_data = {p.player_id: player_dict(p) for p in game_state.avatar_manager.avatars}
        return {
            'players': player_data,
            'score_locations': [(cell.location.x, cell.location.y) for cell in world.score_cells()],
            'pickup_locations': [(cell.location.x, cell.location.y) for cell in world.pickup_cells()],
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
def healthcheck():
    return 'HEALTHY'


@app.route('/player/<player_id>')
def player_data(player_id):
    player_id = int(player_id)
    try:
        code = worker_manager.get_code(player_id)
        correct_auth = worker_manager.check_auth(player_id, flask.request.args.get('auth_token'))
    except KeyError:
        app.logger.warning('Invalid auth_token for user %s', player_id)
        flask.abort(404)
    if not correct_auth:
        app.logger.warning('Unknown user %s', player_id)
        flask.abort(404)
    return flask.jsonify({
        'code': code,
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
    turn_manager = ConcurrentTurnManager(game_state=game_state, end_turn_callback=send_world_update, completion_url=api_url+'complete/?auth_token='+os.environ['auth_token'])
    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    worker_manager = WorkerManagerClass(game_state=game_state, users_url=api_url+'?auth_token='+os.environ['auth_token'], port=port)
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
