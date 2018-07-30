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

        # Session ID is likely to be 19 digits long.
        # TODO: check if alphanumeric and change if required
        self.sid = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                           for _ in range(16))

    def test_socketio_emit_called(self, mocked_socketio,
                                  mocked_game_state):
        import service

        service.world_update_on_connect(self.sid, self.environ)

        self.assertTrue(mocked_socketio.return_value.emit.assert_called_once)

