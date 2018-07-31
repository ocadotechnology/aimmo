from unittest import TestCase
import random
import string
import logging
import mock

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@mock.patch('service.get_game_state', return_value={'foo': 'bar'})
@mock.patch('service.socketioserver')
class TestService(TestCase):

    def setUp(self):
        self.environ = dict()
        self.environ['QUERY_STRING'] = '?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb'

        self.sid = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                           for _ in range(16))

    def tearDown(self):
        import service
        service.session_id_to_avatar_id = {}

    def test_socketio_emit_called(self, mocked_socketio,
                                  mocked_game_state):
        import service

        service.world_update_on_connect(self.sid, self.environ)

        self.assertTrue(mocked_socketio.return_value.emit.assert_called_once)

    def test_socketio_adds_logs_and_makes_correct_call(self, mocked_socketio,
                                                       mocked_game_state):
        import service

        service.world_update_on_connect(self.sid, self.environ)

        mocked_socketio.emit.assert_called_with('game-state',
                                                {'foo': 'bar', 'logs': ''},
                                                room=self.sid)

    def test_matched_session_id_to_avatar_id_mapping(self, mocked_socketio,
                                                     mocked_game_state):
        import service
        mappings = service.session_id_to_avatar_id

        self.assertEqual(len(mappings), 0)

        service.world_update_on_connect(self.sid, self.environ)

        self.assertEqual(len(mappings), 1)
        self.assertTrue(self.sid in mappings)
        self.assertEqual(mappings[self.sid], 1)

    def test_no_match_session_id_to_avatar_id_mapping(self, mocked_socketio,
                                                      mocked_game_state):
        import service
        mappings = service.session_id_to_avatar_id
        self.environ['QUERY_STRING'] = 'corrupted!@$%string123'

        self.assertEqual(len(mappings), 0)

        service.world_update_on_connect(self.sid, self.environ)

        self.assertEqual(len(mappings), 1)
        self.assertTrue(self.sid in mappings)
        self.assertIsNone(mappings[self.sid])

    def test_send_world_update_for_one_user(self, mocked_socketio,
                                            mocked_game_state):
        import service
        mappings = service.session_id_to_avatar_id
        mappings[self.sid] = 1

        service.send_world_update()

        self.assertTrue(mocked_socketio.emit.assert_called_once)
        mocked_socketio.emit.assert_called_with('game-state',
                                                {'foo': 'bar', 'logs': ''},
                                                room=self.sid)

    def test_send_world_update_for_multiple_users(self, mocked_socketio,
                                                  mocked_game_state):
        import service
        mappings = service.session_id_to_avatar_id
        mappings[self.sid] = 1
        mappings['differentsid'] = 2

        service.send_world_update()

        expected_call_one = mock.call('game-state',
                                      {'foo': 'bar', 'logs': ''},
                                      room=self.sid)

        expected_call_two = mock.call('game-state',
                                      {'foo': 'bar', 'logs': ''},
                                      room='differentsid')

        mocked_socketio.emit.assert_has_calls([expected_call_one,
                                               expected_call_two])

