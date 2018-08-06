from unittest import TestCase
import random
import string
import mock

import service
from simulation.logs_provider import LogsProvider


class TestSocketio(TestCase):

    def setUp(self):
        self.environ = {}
        self.mocked_mappings = {}
        self.mocked_logs_provider = LogsProvider()
        self.environ['QUERY_STRING'] = '?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb'

        self.sid = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                           for _ in range(19))

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_socketio_emit_called(self, mocked_socketio,
                                  mocked_game_state):

        service.world_update_on_connect(self.sid, self.environ,
                                        session_id_to_avatar_id=self.mocked_mappings)

        self.assertTrue(mocked_socketio.return_value.emit.assert_called_once)

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_socketio_adds_logs_and_makes_correct_call(self, mocked_socketio,
                                                       mocked_game_state):

        service.world_update_on_connect(self.sid, self.environ,
                                        session_id_to_avatar_id=self.mocked_mappings)

        mocked_socketio.emit.assert_called_with('game-state',
                                                {'foo': 'bar', 'logs': ''},
                                                room=self.sid)

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_matched_session_id_to_avatar_id_mapping(self, mocked_socketio,
                                                     mocked_game_state):

        self.assertEqual(len(self.mocked_mappings), 0)

        service.world_update_on_connect(self.sid, self.environ,
                                        session_id_to_avatar_id=self.mocked_mappings)

        self.assertEqual(len(self.mocked_mappings), 1)
        self.assertTrue(self.sid in self.mocked_mappings)
        self.assertEqual(self.mocked_mappings[self.sid], 1)

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_no_match_session_id_to_avatar_id_mapping(self, mocked_socketio,
                                                      mocked_game_state):
        self.environ['QUERY_STRING'] = 'corrupted!@$%string123'

        self.assertEqual(len(self.mocked_mappings), 0)

        service.world_update_on_connect(self.sid, self.environ,
                                        session_id_to_avatar_id=self.mocked_mappings)

        self.assertEqual(len(self.mocked_mappings), 1)
        self.assertTrue(self.sid in self.mocked_mappings)
        self.assertIsNone(self.mocked_mappings[self.sid])

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_send_world_update_for_one_user(self, mocked_socketio,
                                            mocked_game_state):
        self.mocked_mappings[self.sid] = 1

        service.send_world_update(session_id_to_avatar_id=self.mocked_mappings,
                                  logs_provider=self.mocked_logs_provider)

        self.assertTrue(mocked_socketio.emit.assert_called_once)
        mocked_socketio.emit.assert_called_with('game-state',
                                                {'foo': 'bar', 'logs': ''},
                                                room=self.sid)

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_send_world_update_for_multiple_users(self, mocked_socketio,
                                                  mocked_game_state):
        self.mocked_mappings[self.sid] = 1
        self.mocked_mappings['differentsid'] = 2

        service.send_world_update(session_id_to_avatar_id=self.mocked_mappings,
                                  logs_provider=self.mocked_logs_provider)

        expected_call_one = mock.call('game-state',
                                      {'foo': 'bar', 'logs': ''},
                                      room='differentsid')

        expected_call_two = mock.call('game-state',
                                      {'foo': 'bar', 'logs': ''},
                                      room=self.sid)

        mocked_socketio.emit.assert_has_calls([expected_call_one,
                                               expected_call_two], any_order=True)

