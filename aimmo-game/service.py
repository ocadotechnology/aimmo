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
from simulation.game_runner import GameRunner

eventlet.sleep()
eventlet.monkey_patch()

flask_app = flask.Flask(__name__)
CORS(flask_app, supports_credentials=True)
socketio_server = socketio.Server()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GameAPI(object):
    def __init__(self, worker_manager, game_state, logs, have_avatars_code_updated):
        self.worker_manager = worker_manager
        self.logs = logs
        self.game_state = game_state
        self._sid_to_avatar_id = {}
        self.have_avatars_code_updated = have_avatars_code_updated

        self.register_endpoints()

    def register_endpoints(self):
        self.register_player_data_view()
        self.register_world_update_on_connect()
        self.register_remove_session_id_from_mappings()
        self.register_healthcheck()

    def register_healthcheck(self):
        @flask_app.route('/game-<game_id>')
        def healthcheck(game_id):
            return 'HEALTHY'

    def register_player_data_view(self):
        @flask_app.route('/player/<player_id>')
        def player_data(player_id):
            player_id = int(player_id)
            return flask.jsonify({
                'code': self.worker_manager.get_code(player_id),
                'options': {},
                'state': None,
            })

        return player_data

    def register_world_update_on_connect(self):
        @socketio_server.on('connect')
        def world_update_on_connect(sid, environ):
            self._sid_to_avatar_id[sid] = None

            query = environ['QUERY_STRING']
            self._find_avatar_id_from_query(sid, query)
            self.send_updates()

        return world_update_on_connect

    def register_remove_session_id_from_mappings(self):
        @socketio_server.on('disconnect')
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
        self._send_have_avatars_code_updated()

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

    def _send_have_avatars_code_updated(self):
        for sid, avatar_id in self._sid_to_avatar_id.iteritems():
            if self.have_avatars_code_updated.get(avatar_id, False):
                socketio_server.emit('feedback-avatar-updated', room=sid)


def run_game(port):
    print("Running game...")
    settings = pickle.loads(os.environ['settings'])
    api_url = os.environ.get('GAME_API_URL', 'http://localhost:8000/aimmo/api/games/')
    generator = getattr(map_generator, settings['GENERATOR'])(settings)
    player_manager = AvatarManager()

    communicator = Communicator(api_url=api_url, completion_url=api_url + 'complete/')
    game_state = generator.get_game_state(player_manager)

    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    worker_manager = WorkerManagerClass(port=port)

    logs = Logs()
    have_avatars_code_updated = {}

    game_api = GameAPI(worker_manager, game_state, logs, have_avatars_code_updated)

    turn_manager = ConcurrentTurnManager(end_turn_callback=game_api.send_updates,
                                         communicator=communicator,
                                         game_state=game_state,
                                         logs=logs,
                                         have_avatars_code_updated=have_avatars_code_updated)

    game_runner = GameRunner(worker_manager=worker_manager,
                             game_state=game_state,
                             communicator=communicator)

    game_runner.start()
    turn_manager.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    host, port = sys.argv[1], int(sys.argv[2])
    socket_app = socketio.Middleware(socketio_server, flask_app,
                                     socketio_path=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))

    run_game(port)
    eventlet.wsgi.server(eventlet.listen((host, port)), socket_app, debug=False)
