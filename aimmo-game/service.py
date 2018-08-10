#!/usr/bin/env python

import cPickle as pickle
import logging
import os
import sys
import eventlet
import flask
import socketio as SocketIO
from urlparse import parse_qs
from flask_cors import CORS

from simulation import map_generator
from simulation.turn_manager import ConcurrentTurnManager
from simulation.logs_provider import LogsProvider
from simulation.game_state_provider import GameStateProvider
from simulation.avatar.avatar_manager import AvatarManager
from simulation.worker_managers import WORKER_MANAGERS
from simulation.pickups import pickups_update
from simulation.communicator import Communicator

eventlet.sleep()
eventlet.monkey_patch()

app = flask.Flask(__name__)
CORS(app, supports_credentials=True)
socketio_server = SocketIO.Server()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

_default_worker_manager = None
_default_state_provider = GameStateProvider()
_default_logs_provider = LogsProvider()
_default_session_id_to_avatar_id_mappings = {}


@app.route('/game-<game_id>')
def healthcheck(game_id):
    return 'HEALTHY'


@app.route('/player/<player_id>')
def player_data(player_id):
    player_id = int(player_id)
    return flask.jsonify({
        'code': _default_worker_manager.get_code(player_id),
        'options': {},
        'state': None,
    })


@socketio_server.on('connect')
def world_update_on_connect(sid, environ,
                            session_id_to_avatar_id=_default_session_id_to_avatar_id_mappings):
    game_state = get_game_state()
    session_id_to_avatar_id[sid] = None

    query = environ['QUERY_STRING']
    _find_avatar_id_from_query(sid, query,
                               session_id_to_avatar_id=session_id_to_avatar_id)
    send_updates()


@socketio_server.on('disconnect')
def remove_session_id_from_mappings(sid,
                                    session_id_to_avatar_id=_default_session_id_to_avatar_id_mappings):
    LOGGER.info("Socket disconnected for session id:{}. ".format(sid))
    try:
        del session_id_to_avatar_id[sid]
    except KeyError:
        pass


def send_logs(session_id_to_avatar_id, logs_provider):
    for sid, avatar_id in session_id_to_avatar_id.iteritems():
        avatar_logs = logs_provider.get_user_logs(avatar_id)
        socketio_server.emit(
            'log',
            avatar_logs,
            room=sid,
        )


def send_game_state(session_id_to_avatar_id):
    game_state = get_game_state()
    for sid, avatar_id in session_id_to_avatar_id.iteritems():
        socketio_server.emit(
            'game-state',
            game_state,
            room=sid,
        )


def send_updates(session_id_to_avatar_id=_default_session_id_to_avatar_id_mappings,
                      logs_provider=_default_logs_provider):
    send_game_state(session_id_to_avatar_id)
    send_logs(session_id_to_avatar_id, logs_provider)



def get_game_state(state_provider=_default_state_provider):
    with state_provider as game_state:
        world_map = game_state.world_map

        return {
            'era': "less_flat",
            'southWestCorner': world_map.get_serialised_south_west_corner(),
            'northEastCorner': world_map.get_serialised_north_east_corner(),
            'players': game_state.avatar_manager.players_update()['players'],
            'pickups': pickups_update(world_map)['pickups'],
            'scoreLocations': (game_state.world_map.
                score_location_update()['scoreLocations']),
            'obstacles': world_map.obstacles_update()['obstacles']
        }


def to_cell_type(cell):
    if not cell.habitable:
        return 1
    if cell.generates_score:
        return 2
    return 0


def player_dict(avatar):
    return {
        'id': avatar.player_id,
        'x': avatar.location.x,
        'y': avatar.location.y,
        'health': avatar.health,
        'score': avatar.score,
        'rotation': 0,
        "colours": {
            "bodyStroke": "#0ff",
            "bodyFill": "#%06x" % (avatar.player_id * 4999),
            "eyeStroke": "#aff",
            "eyeFill": "#eff",
        }
    }


def _find_avatar_id_from_query(session_id, query_string,
                               session_id_to_avatar_id):
    """
    :param session_id: Int with the session id
    :param query_string: String from the environment settings,
    usually located as the key 'QUERY_STRING'.
    """
    parsed_qs = parse_qs(query_string)

    try:
        avatar_id = parsed_qs['avatar_id'][0]
        session_id_to_avatar_id[session_id] = avatar_id
    except KeyError:
        LOGGER.error("No avatar ID found. User may not be authorised ")


def run_game(port):
    global _default_worker_manager, _default_state_provider, _default_logs_provider

    print("Running game...")
    settings = pickle.loads(os.environ['settings'])
    api_url = os.environ.get('GAME_API_URL', 'http://localhost:8000/aimmo/api/games/')
    generator = getattr(map_generator, settings['GENERATOR'])(settings)
    player_manager = AvatarManager()

    communicator = Communicator(api_url=api_url, completion_url=api_url+'complete/')
    game_state = generator.get_game_state(player_manager)
    turn_manager = ConcurrentTurnManager(game_state=game_state,
                                         end_turn_callback=send_updates,
                                         communicator=communicator,
                                         state_provider=_default_state_provider,
                                         logs_provider=_default_logs_provider)
    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    _default_worker_manager = WorkerManagerClass(game_state=game_state,
                                                 communicator=communicator,
                                                 port=port)
    _default_worker_manager.start()
    turn_manager.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    host, port = sys.argv[1], int(sys.argv[2])
    app = SocketIO.Middleware(socketio_server, app, socketio_path=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))

    run_game(port)
    eventlet.wsgi.server(eventlet.listen((host, port)), app, debug=False)
