from unittest import TestCase
import random
import string
import mock

import service
from simulation.worker_managers.local_worker_manager import LocalWorkerManager
from simulation.game_runner import GameRunner


class MockGameState(object):
    def serialise(self):
        return {'foo': 'bar'}


class MockedSocketIOServer(mock.MagicMock):
    """ Decorator function that just returns the function. Needed because we decorate
        functions in the GameAPI."""
    def on(self, event):
        def decorator(func):
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)
            return wrapper
        return decorator


class TestSocketIO(TestCase):
    def setUp(self):
        self.environ = {'QUERY_STRING': 'avatar_id=1&EIO=3&transport=polling&t=MJhoMgb'}
        self.game_api = self.create_game_api()
        self.mocked_mappings = self.game_api._socket_session_id_to_player_id
        self.sid = ''.join(random.choice(string.ascii_uppercase +
                                         string.ascii_lowercase +
                                         string.digits)
                           for _ in range(19))

    @mock.patch('service.flask_app')
    def create_game_api(self, flask_app):
        game_runner = GameRunner(worker_manager_class=LocalWorkerManager,
                                 game_state_generator=lambda avatar_manager: MockGameState(),
                                 django_api_url='http://test',
                                 port='0000')
        return service.GameAPI(game_state=game_runner.game_state,
                               worker_manager=game_runner.worker_manager)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_socketio_emit_called(self, mocked_socketio, flask_app):
        self.game_api.worker_manager.add_new_worker(1)
        self.game_api.register_world_update_on_connect()(self.sid, self.environ)

        self.assertTrue(mocked_socketio.return_value.emit.assert_called_once)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_matched_session_id_to_avatar_id_mapping(self, mocked_socketio, flask_app):
        self.assertEqual(len(self.mocked_mappings), 0)

        self.game_api.worker_manager.add_new_worker(1)
        self.game_api.register_world_update_on_connect()(self.sid, self.environ)

        self.assertEqual(len(self.mocked_mappings), 1)
        self.assertTrue(self.sid in self.mocked_mappings)
        self.assertEqual(int(self.mocked_mappings[self.sid]), 1)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_no_match_session_id_to_avatar_id_mapping(self, mocked_socketio, flask_app):
        self.environ['QUERY_STRING'] = 'corrupted!@$%string123'

        self.assertEqual(len(self.mocked_mappings), 0)

        self.game_api.worker_manager.add_new_worker(1)
        self.game_api.register_world_update_on_connect()(self.sid, self.environ)

        self.assertEqual(len(self.mocked_mappings), 0)
        self.assertFalse(self.sid in self.mocked_mappings)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_send_updates_for_one_user(self, mocked_socketio, flask_app):
        self.mocked_mappings[self.sid] = 1
        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        worker = self.game_api.worker_manager.player_id_to_worker[self.mocked_mappings[self.sid]]
        worker.log = 'Logs one'

        self.game_api.send_updates()

        game_state_call = mock.call('game-state', {'foo': 'bar'}, room=self.sid)
        log_call = mock.call('log', 'Logs one', room=self.sid)

        mocked_socketio.emit.assert_has_calls([game_state_call, log_call], any_order=True)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_no_logs_not_emitted(self, mocked_socketio, flask_app):
        """ If there are no logs for an avatar, no logs should be emitted. """
        self.mocked_mappings[self.sid] = 1
        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        self.game_api.send_updates()

        mocked_socketio.emit.assert_called_once_with('game-state', {'foo': 'bar'}, room=self.sid)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_empty_logs_not_emitted(self, mocked_socketio, flask_app):
        """ If the logs are an empty sting, no logs should be emitted. """
        self.mocked_mappings[self.sid] = 1

        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        worker = self.game_api.worker_manager.player_id_to_worker[self.mocked_mappings[self.sid]]
        worker.logs = ''
        self.game_api.send_updates()

        mocked_socketio.emit.assert_called_once_with('game-state', {'foo': 'bar'}, room=self.sid)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_send_updates_for_multiple_users(self, mocked_socketio, flask_app):
        self.mocked_mappings[self.sid] = 1
        self.mocked_mappings['differentsid'] = 2

        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        self.game_api.worker_manager.add_new_worker(self.mocked_mappings['differentsid'])
        worker_one = self.game_api.worker_manager.player_id_to_worker[self.mocked_mappings[self.sid]]
        worker_two = self.game_api.worker_manager.player_id_to_worker[self.mocked_mappings['differentsid']]
        worker_one.log = 'Logs one'
        worker_two.log = 'Logs two'

        self.game_api.send_updates()

        user_one_game_state_call = mock.call('game-state', {'foo': 'bar'}, room=self.sid)
        user_two_game_state_call = mock.call('game-state', {'foo': 'bar'}, room='differentsid')
        user_one_log_call = mock.call('log', 'Logs one', room=self.sid)
        user_two_log_call = mock.call('log', 'Logs two', room='differentsid')

        mocked_socketio.emit.assert_has_calls([user_one_game_state_call,
                                               user_two_game_state_call,
                                               user_one_log_call,
                                               user_two_log_call], any_order=True)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_send_code_changed_flag(self, mocked_socketio, flask_app):
        self.mocked_mappings[self.sid] = 1
        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        worker = self.game_api.worker_manager.player_id_to_worker[self.mocked_mappings[self.sid]]
        worker.has_code_updated = True
        self.game_api.send_updates()

        user_game_state_call = mock.call('game-state', {'foo': 'bar'}, room=self.sid)
        user_game_code_changed_call = mock.call('feedback-avatar-updated', room=self.sid)

        mocked_socketio.emit.assert_has_calls([user_game_state_call, user_game_code_changed_call], any_order=True)

    @mock.patch('service.flask_app')
    @mock.patch('service.socketio_server', new_callable=MockedSocketIOServer)
    def test_send_false_flag_not_sent(self, mocked_socketio, flask_app):
        self.mocked_mappings[self.sid] = 1
        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        worker = self.game_api.worker_manager.player_id_to_worker[self.mocked_mappings[self.sid]]
        worker.has_code_updated = False
        self.game_api.send_updates()

        mocked_socketio.emit.assert_called_once_with('game-state', {'foo': 'bar'}, room=self.sid)

    def test_remove_session_id_on_disconnect(self):
        self.mocked_mappings[self.sid] = 1
        self.assertEqual(len(self.mocked_mappings), 1)
        self.assertTrue(self.sid in self.mocked_mappings)
        self.assertEqual(self.mocked_mappings[self.sid], 1)

        self.game_api.register_remove_session_id_from_mappings()(sid=self.sid)

        self.assertFalse(self.sid in self.mocked_mappings)
        self.assertEqual(len(self.mocked_mappings), 0)
