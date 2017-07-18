from __future__ import absolute_import

from server import MockServer
from server import Runner
from unittest import TestCase

import os
import subprocess
import time
import signal
import requests

import sys
sys.path.append('../../')

from httmock import HTTMock

# Note: The kubernates setup works only from the root of the directory.
def run_command_async(args, cwd="."):
    p = subprocess.Popen(args, cwd=cwd)
    return p

import cPickle as pickle
from json import dumps

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

# Request mockeries

class RequestMock(object):
    def __init__(self, num_games):
        self.value = self._generate_response(num_games)
        self.urls_requested = []

    def _generate_response(self, num_games):
        pass

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)

class GameCreatorRequestMock(RequestMock):
    def _generate_response(self, num_games):
        return {
            str(i): {
                'name': 'Level1',
                'settings': pickle.dumps(DEFAULT_LEVEL_SETTINGS)
            } for i in xrange(num_games)
        }

class GameRequestMock(RequestMock):
    def _generate_response(self, num_games):
        return DEFAULT_AI

################################################################################

# See definition of a runner in mock_server.py

class GameCreatorRunner(Runner):
    def apply(self, received):
        mocker = GameCreatorRequestMock(1)
        with HTTMock(mocker):
            ans = requests.get(self.binder._SERVER_URL + received)
            self.binder.assertEqual(len(mocker.urls_requested), 1)
            self.binder.assertEqual("/players/api/games/" in mocker.urls_requested[0], True)
            return ans.text

class GameRunner(Runner):
    def apply(self, received):
        mocker = GameRequestMock(1)
        with HTTMock(mocker):
            ans = requests.get(self.binder._SERVER_URL + received)
            self.binder.assertEqual(len(mocker.urls_requested), 1)
            self.binder.assertEqual("/players/api/games/0/" in mocker.urls_requested[0], True)
            return ans.text

class TurnRunner(Runner):
    def apply(self, received):
        return "NotImplemented"

################################################################################

class TestService(TestCase):
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'aimmo-game-creator', 'service.py')

    def __setup_environment(self):
        os.environ['AIMMO_MODE'] = 'threads'
        os.environ['WORKER_MANAGER'] = 'local'
        os.environ['GAME_API_URL'] = 'http://localhost:8000/players/api/games/'

        self._SERVER_URL = 'http://localhost:8000/'
        self._SERVER_PORT = '8000'

    def __build_test(self, runners, kubernetes=False):
        try:
            if kubernetes:
                # TODO: proper start-up
                os.system("minikube delete")
                os.system("minikube start --vm-driver=kvm")

                game = run_command_async(['python', "minikube.py"], self._SCRIPT_LOCATION)
            else:
                game = run_command_async(['python', self._SERVICE_PY, self._SERVER_URL, self._SERVER_PORT])

            server = MockServer()
            for runner, times in runners:
                print "Running " + str(runner) + " " + str(times) + " times"
                server.register_runner(runner)
                server.run(times)
                server.clear_runners()

        finally:
            if kubernetes:
                os.system("pkill -TERM -P " + str(game.pid))
                os.kill(game.pid, signal.SIGKILL)
                os.system("minikube delete")
            else:
                os.system("pkill -TERM -P " + str(game.pid))
                os.kill(game.pid, signal.SIGKILL)


    def setUp(self):
        self.__setup_resources()
        self.__setup_environment()

    def test_killing_creator_kills_game(self):
        try:
            game = run_command_async(['python', self._SERVICE_PY, self._SERVER_URL, self._SERVER_PORT])
        finally:
            os.system("pkill -TERM -P " + str(game.pid))
            os.kill(game.pid, signal.SIGKILL)

    def test_games_get_generated(self):
        self.__build_test([
            (GameCreatorRunner(self), 1),
            (GameRunner(self), 1)
        ], False)

    # TODO: We need to add a seam in the server so we can use this communication tool and further tests
    def test_turns_run(self):
        self.__build_test([
            (GameCreatorRunner(self), 1),
            (GameRunner(self), 1)
        ], False)

    def test_games_get_generated_repeatedly(self):
        # to ensure there are no concurrency issues, we shall run a test multiple
        # times; TODO: see effect of local networking
        times = 10
        for i in xrange(times):
            self.test_games_get_generated()

    def ktest_games_get_generated_kubernates(self):
        self.__build_test([
            (GameCreatorRunner(self), 1),
            (GameRunner(self), 1),
            (TurnRunner(self), 1)
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

    # TODO: not yet fully supported locally; probably an environment problem
    # as server does not communicate with the cluster
    # suite.addTest(TestService("test_games_get_generated_kubernates"))

    return suite

def main():
    suite = get_test_suite()

    runner = TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    main()
