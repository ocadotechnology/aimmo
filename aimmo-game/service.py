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
from simulation.worker_managers import WORKER_MANAGERS
from simulation.game_runner import GameRunner

eventlet.sleep()
eventlet.monkey_patch()

flask_app = flask.Flask(__name__)
CORS(flask_app, supports_credentials=True)
socketio_server = socketio.Server()

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GameAPI(object):
    def __init__(self, game_state, worker_manager):
        self._socket_session_id_to_player_id = {}
        self.register_endpoints()
        self.worker_manager = worker_manager
        self.game_state = game_state

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
            query = environ['QUERY_STRING']
            self._find_avatar_id_from_query(sid, query)
            self.send_updates()

        return world_update_on_connect

    def register_remove_session_id_from_mappings(self):
        @socketio_server.on('disconnect')
        def remove_session_id_from_mappings(sid):
            LOGGER.info("Socket disconnected for session id:{}. ".format(sid))
            try:
                del self._socket_session_id_to_player_id[sid]
            except KeyError:
                pass

        return remove_session_id_from_mappings

    def send_updates(self):
        self._send_game_state()
        player_id_to_worker = self.worker_manager.player_id_to_worker
        self._send_logs(player_id_to_worker)
        self._send_have_avatars_code_updated(player_id_to_worker)

    def _find_avatar_id_from_query(self, session_id, query_string):
        """
        :param session_id: Int with the session id
        :param query_string: String from the environment settings,
        usually located as the key 'QUERY_STRING'.
        """
        parsed_qs = parse_qs(query_string)

        try:
            avatar_id = int(parsed_qs['avatar_id'][0])
            self._socket_session_id_to_player_id[session_id] = avatar_id
        except ValueError:
            LOGGER.error("Avatar ID could not be casted into an integer")
        except KeyError:
            LOGGER.error("No avatar ID found. User may not be authorised ")
            LOGGER.error("query_string: " + query_string)

    def _send_logs(self, player_id_to_workers):
        def should_send_logs(logs):
            LOGGER.info("should_send_logs: " + str(logs))

            return logs is not None and logs != ''

        socket_session_id_to_player_id_copy = self._socket_session_id_to_player_id.copy()
        for sid, player_id in socket_session_id_to_player_id_copy.iteritems():
            avatar_logs = player_id_to_workers[player_id].log
            if should_send_logs(avatar_logs):
                socketio_server.emit('log', avatar_logs, room=sid)

    def _send_game_state(self):
        serialised_game_state = self.game_state.serialise()
        socket_session_id_to_player_id_copy = self._socket_session_id_to_player_id.copy()
        for sid, player_id in socket_session_id_to_player_id_copy.iteritems():
            socketio_server.emit('game-state', serialised_game_state, room=sid)

    def _send_have_avatars_code_updated(self, player_id_to_workers):
        socket_session_id_to_player_id_copy = self._socket_session_id_to_player_id.copy()
        for sid, player_id in socket_session_id_to_player_id_copy.iteritems():
            if player_id_to_workers[player_id].has_code_updated:
                socketio_server.emit('feedback-avatar-updated', room=sid)


def create_runner(port):
    settings = pickle.loads(os.environ['settings'])
    generator = getattr(map_generator, settings['GENERATOR'])(settings)
    worker_manager_class = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]

    return GameRunner(worker_manager_class=worker_manager_class,
                      game_state_generator=generator.get_game_state,
                      django_api_url=os.environ.get('GAME_API_URL', 'http://localhost:8000/aimmo/api/games/'),
                      port=port)


def run_game(port):
    game_runner = create_runner(port)
    game_api = GameAPI(game_state=game_runner.game_state,
                       worker_manager=game_runner.worker_manager)
    game_runner.set_end_turn_callback(game_api.send_updates)
    game_runner.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    host, port = sys.argv[1], int(sys.argv[2])
    socket_app = socketio.Middleware(socketio_server, flask_app,
                                     socketio_path=os.environ.get('SOCKETIO_RESOURCE', 'socket.io'))

    run_game(port)
    eventlet.wsgi.server(eventlet.listen((host, port)), socket_app, debug=False)
