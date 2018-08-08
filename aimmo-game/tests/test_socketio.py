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
        self.environ['QUERY_STRING'] = 'avatar_id=1&EIO=3&transport=polling&t=MJhoMgb'

        self.sid = ''.join(random.choice(string.ascii_uppercase +
                                         string.ascii_lowercase +
                                         string.digits)
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
    def test_matched_session_id_to_avatar_id_mapping(self, mocked_socketio,
                                                     mocked_game_state):
        self.assertEqual(len(self.mocked_mappings), 0)

        service.world_update_on_connect(self.sid, self.environ,
                                        session_id_to_avatar_id=self.mocked_mappings)

        self.assertEqual(len(self.mocked_mappings), 1)
        self.assertTrue(self.sid in self.mocked_mappings)
        self.assertEqual(int(self.mocked_mappings[self.sid]), 1)

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
    def test_send_updates_for_one_user(self, mocked_socketio,
                                       mocked_game_state):
        self.mocked_mappings[self.sid] = 1

        service.send_updates(session_id_to_avatar_id=self.mocked_mappings,
                             logs_provider=self.mocked_logs_provider)

        game_state_call = mock.call('game-state', {'foo': 'bar'}, room=self.sid)
        log_call = mock.call('log', None, room=self.sid)

        mocked_socketio.emit.assert_has_calls([game_state_call, log_call], any_order=True)

    @mock.patch('service.get_game_state', return_value={'foo': 'bar'})
    @mock.patch('service.socketio_server')
    def test_send_updates_for_multiple_users(self, mocked_socketio,
                                             mocked_game_state):
        self.mocked_mappings[self.sid] = 1
        self.mocked_mappings['differentsid'] = 2

        service.send_updates(session_id_to_avatar_id=self.mocked_mappings,
                             logs_provider=self.mocked_logs_provider)

        user_one_game_state_call = mock.call('game-state',
                                             {'foo': 'bar'},
                                             room=self.sid)

        user_two_game_state_call = mock.call('game-state',
                                             {'foo': 'bar'},
                                             room='differentsid')

        user_one_log_call = mock.call('log',
                                      None,
                                      room=self.sid)

        user_two_log_call = mock.call('log',
                                      None,
                                      room='differentsid')

        mocked_socketio.emit.assert_has_calls([user_one_game_state_call,
                                               user_two_game_state_call,
                                               user_one_log_call,
                                               user_two_log_call], any_order=True)

    def test_remove_session_id_on_disconnect(self):
        self.mocked_mappings[self.sid] = 1
        self.assertEqual(len(self.mocked_mappings), 1)
        self.assertTrue(self.sid in self.mocked_mappings)
        self.assertEqual(self.mocked_mappings[self.sid], 1)

        service.remove_session_id_from_mappings(sid=self.sid,
                                                session_id_to_avatar_id=self.mocked_mappings)

        self.assertFalse(self.sid in self.mocked_mappings)
        self.assertEqual(len(self.mocked_mappings), 0)
