#!/usr/bin/env python

import cPickle as pickle
import logging
import os
import sys
from urlparse import parse_qs

import eventlet
import flask
import socketio
from flask_cors import CORS

from simulation import map_generator
from simulation.turn_manager import ConcurrentTurnManager
from simulation.logs import Logs
from simulation.avatar.avatar_manager import AvatarManager
from simulation.worker_managers import WORKER_MANAGERS
from simulation.communicator import Communicator

eventlet.sleep()
eventlet.monkey_patch()

flask_app = flask.Flask(__name__)
CORS(flask_app, supports_credentials=True)
socketio_server = socketio.Server()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@flask_app.route('/game-<game_id>')
def healthcheck(game_id):
    return 'HEALTHY'


class GameAPI(object):
    def __init__(self, worker_manager, game_state, logs, src_changed_flags):
        self.worker_manager = worker_manager
        self.logs = logs
        self.game_state = game_state
        self._sid_to_avatar_id = {}
        self.src_changed_flags = src_changed_flags

    def make_player_data_view(self):
        """This method will get registered at /player/<player_id>"""
        def player_data(player_id):
            player_id = int(player_id)
            return flask.jsonify({
                'code': self.worker_manager.get_code(player_id),
                'options': {},
                'state': None,
            })
        return player_data

    def make_world_update_on_connect(self):
        """This method will get registered for connect on socketio_server"""
        def world_update_on_connect(sid, environ):
            self._sid_to_avatar_id[sid] = None

            query = environ['QUERY_STRING']
            self._find_avatar_id_from_query(sid, query)
            self.send_updates()

        return world_update_on_connect

    def make_remove_session_id_from_mappings(self):
        """This method will get registered for disconnect on socketio_server"""
        def remove_session_id_from_mappings(sid):
            LOGGER.info("Socket disconnected for session id:{}. ".format(sid))
            try:
                del self._sid_to_avatar_id[sid]
            except KeyError:
                pass

        return remove_session_id_from_mappings

    def send_updates(self):
        self._send_game_state()
        self._send_logs()
        self._send_src_changed_flags()

    def _find_avatar_id_from_query(self, session_id, query_string):
        """
        :param session_id: Int with the session id
        :param query_string: String from the environment settings,
        usually located as the key 'QUERY_STRING'.
        """
        parsed_qs = parse_qs(query_string)

        try:
            avatar_id = int(parsed_qs['avatar_id'][0])
            self._sid_to_avatar_id[session_id] = avatar_id
        except ValueError:
            LOGGER.error("Avatar ID could not be casted into an integer")
        except KeyError:
            LOGGER.error("No avatar ID found. User may not be authorised ")

    def _send_logs(self):
        def should_send_logs(logs):
            return logs is not None and logs != ''

        for sid, avatar_id in self._sid_to_avatar_id.iteritems():
            avatar_logs = self.logs.get_user_logs(avatar_id)
            if should_send_logs(avatar_logs):
                socketio_server.emit('log', avatar_logs, room=sid)

    def _send_game_state(self):
        serialised_game_state = self.game_state.serialise()
        for sid, avatar_id in self._sid_to_avatar_id.iteritems():
            socketio_server.emit('game-state', serialised_game_state, room=sid)

    def _send_src_changed_flags(self):
        for sid, avatar_id in self._sid_to_avatar_id.iteritems():
            if self.src_changed_flags.get(avatar_id, False):
                socketio_server.emit('src-changed', self.src_changed_flags[avatar_id], room=sid)


def run_game(port):
    print("Running game...")
    settings = pickle.loads(os.environ['settings'])
    api_url = os.environ.get('GAME_API_URL', 'http://localhost:8000/aimmo/api/games/')
    generator = getattr(map_generator, settings['GENERATOR'])(settings)
    player_manager = AvatarManager()

    communicator = Communicator(api_url=api_url, completion_url=api_url + 'complete/')
    game_state = generator.get_game_state(player_manager)

    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    worker_manager = WorkerManagerClass(game_state=game_state, communicator=communicator, port=port)

    logs = Logs()
    src_changed_flags = {}

    game_api = GameAPI(worker_manager, game_state, logs, src_changed_flags)

    turn_manager = ConcurrentTurnManager(end_turn_callback=game_api.send_updates,
                                         communicator=communicator,
                                         game_state=game_state,
                                         logs=logs,
                                         src_changed_flags=src_changed_flags)

    flask_app.add_url_rule('/player/<player_id>', 'player_data', game_api.make_player_data_view())
    socketio_server.on('connect', game_api.make_world_update_on_connect())
    socketio_server.on('disconnect', game_api.make_remove_session_id_from_mappings())

    worker_manager.start()
    turn_manager.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    host, port = sys.argv[1], int(sys.argv[2])
    socket_app = socketio.Middleware(socketio_server, flask_app,
                                     socketio_path=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))

    run_game(port)
    eventlet.wsgi.server(eventlet.listen((host, port)), socket_app, debug=False)
