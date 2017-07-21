from __future__ import absolute_import

from server import MockServer
from server import ConnectionProxy
from unittest import TestCase
from unittest import skip

import time
import signal
import requests

import os
import subprocess
import sys
from httmock import HTTMock

import cPickle as pickle
from json import dumps

from misc import run_command_async, kill_process_tree

################################################################################

# Default setting for the AI code and the default API settings used to mock
# the Django server. This will act as a client and the requests and responses
# should be verified using proxies as explained below and in server.py

DEFAULT_LEVEL_SETTINGS = {
    'TARGET_NUM_CELLS_PER_AVATAR': 16.0,
    'GENERATOR': 'Level1',
    'START_HEIGHT': 11,
    'TARGET_NUM_PICKUPS_PER_AVATAR': 0.5,
    'START_WIDTH': 11,
    'SCORE_DESPAWN_CHANCE': 0.02,
    'TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR': 0.5,
    'OBSTACLE_RATIO': 0.1,
    'PICKUP_SPAWN_CHANCE': 0.02
}

DEFAULT_AI = {
    'main': {
        'parameters': [],
        'main_avatar': None,
        'users': [
            { 'code':
"""class Avatar(object):
        def handle_turn(self, world_view, events):
            from simulation.action import MoveAction
            from simulation.direction import ALL_DIRECTIONS

            import random
            return MoveAction(random.choice(ALL_DIRECTIONS))""",
             'id': 1}]}}

################################################################################


class RequestMock(object):
    """
        Request mockery that can be used in a proxy.
    """
    def __init__(self, num_games):
        self.value = self._generate_response(num_games)
        self.urls_requested = []

    def _generate_response(self, num_games):
        pass

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)

class GameCreatorRequestMock(RequestMock):
    """
        Mockery to expose a set of games.
    """
    def _generate_response(self, num_games):
        return {
            str(i): {
                'name': 'Level1',
                'settings': pickle.dumps(DEFAULT_LEVEL_SETTINGS)
            } for i in xrange(num_games)
        }

class GameRequestMock(RequestMock):
    """
        Mockery to expose an AI behaviour.
    """
    def _generate_response(self, num_games):
        return DEFAULT_AI

################################################################################

# See definition of a proxy in mock_server.py

class GameCreatorProxy(ConnectionProxy):
    """
        Proxy for the game creator. Asserts that only the games resouce has
        been accessed and returns a valid list of games.
    """
    def apply(self, received):
        mocker = GameCreatorRequestMock(1)
        with HTTMock(mocker):
            ans = requests.get(self.binder._SERVER_URL + received)
            self.binder.assertEqual(len(mocker.urls_requested), 1)
            self.binder.assertEqual("/players/api/games/" in mocker.urls_requested[0], True)
            return ans.text

class GameProxy(ConnectionProxy):
    """
        Proxy for the game. Asserts that only the specific game resouce has
        been accessed and returns a valid list of users.
    """
    def apply(self, received):
        mocker = GameRequestMock(1)
        with HTTMock(mocker):
            ans = requests.get(self.binder._SERVER_URL + received)
            self.binder.assertEqual(len(mocker.urls_requested), 1)
            print mocker.urls_requested[0]
            self.binder.assertEqual("/players/api/games/0/" in mocker.urls_requested[0], True)
            return ans.text

# TODO: for more complex tests a seam has to be exposed or socket.io needs to be supported
class TurnProxy(ConnectionProxy):
    def apply(self, received):
        return "NotImplemented"

################################################################################

class TestService(TestCase):
    """
        Test service that verifies the creating of the games and workers cluster.
        Uses the MockServer class insted of the Django client.
        This is a more lightweight integration test that only tests the backend connections.

        Usage:
          * add a test like this:
              self.__build_test([
                  (GameCreatorProxy(self), 1), # pair of proxy and turns
                  (GameProxy(self), 1)
              ], False)                        # set True for kubernates

          * the service runs minikube/localhost for testing
          * kubernates tests should be named: "ktest_..."
          * localhost tests should be named: "test_..."
          * new proxies and can be added to the tests -- see the proxies above for details
    """
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'aimmo-game-creator', 'service.py')

    def __setup_environment(self):
        os.environ['AIMMO_MODE'] = 'threads'
        os.environ['WORKER_MANAGER'] = 'local'
        os.environ['GAME_API_URL'] = 'http://localhost:8000/players/api/games/'

        self._SERVER_URL = 'http://localhost:8000/'
        self._SERVER_PORT = '8000'

    def __build_test(self, proxies, kubernetes=False):
        try:
            if kubernetes:
                # TODO: proper start-up
                os.system("minikube delete")
                os.system("minikube start --vm-driver=kvm")

                game = run_command_async(['python', "minikube.py"], self._SCRIPT_LOCATION)
            else:
                game = run_command_async(['python', self._SERVICE_PY, self._SERVER_URL, self._SERVER_PORT])

            server = MockServer()
            for proxy, times in proxies:
                print "Running " + str(proxy) + " " + str(times) + " times"
                server.register_proxy(proxy)
                server.run(times)
                server.clear_proxies()

        finally:
            if kubernetes:
                os.system("pkill -TERM -P " + str(game.pid))
                os.kill(game.pid, signal.SIGKILL)
                os.system("minikube delete")
            else:
                time.sleep(1)
                kill_process_tree(game.pid)

    def setUp(self):
        self.__setup_resources()
        self.__setup_environment()

    def test_local_killing_creator_kills_game(self):
        try:
            game = run_command_async(['python', self._SERVICE_PY, self._SERVER_URL, self._SERVER_PORT])
        finally:
            time.sleep(1)
            kill_process_tree(game.pid)

    def test_local_games_get_generated(self):
        self.__build_test([
            (GameCreatorProxy(self), 1),
            (GameProxy(self), 1)
        ], False)

    def test_local_turns_run(self):
        self.__build_test([
            (GameCreatorProxy(self), 1),
            (GameProxy(self), 1)
        ], False)

    def test_local_games_get_generated_repeatedly(self):
        times = 5
        for i in xrange(times):
            self.test_local_games_get_generated()

    @skip("temporary")
    def test_kube_games_get_generated_kubernates(self):
        self.__build_test([
            (GameCreatorProxy(self), 1),
            (GameConnectionProxy(self), 1),
            (TurnProxy(self), 1)
        ], True)

from unittest import TestSuite
from unittest import TextTestRunner

# We use this locally as it is simple to work on test development
def get_test_suite():
    suite = TestSuite()

    suite.addTest(TestService("test_killing_creator_kills_game"))
    suite.addTest(TestService("test_games_get_generated"))
    suite.addTest(TestService("test_games_get_generated_repeatedly"))
    suite.addTest(TestService("test_turns_run"))

    return suite

def main():
    suite = get_test_suite()

    proxy = TextTestRunner()
    proxy.run(suite)

if __name__ == "__main__":
    main()
