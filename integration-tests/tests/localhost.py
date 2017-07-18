from __future__ import absolute_import

from server import MockServer
from server import Runner
from unittest import TestCase

import os
import subprocess
import time
import signal
import requests

from httmock import HTTMock

# import sys
# # Add the ptdraft folder path to the sys.path list
# sys.path.append('../../')
#
# import importlib
# mockery = importlib.import_module("aimmo-game-creator.tests.test_worker_manager")

def run_command_async(args, cwd="."):
    p = subprocess.Popen(args, cwd=cwd)
    return p

import cPickle as pickle
from json import dumps

DEFAULT_LEVEL_SETTINGS = {
    'TARGET_NUM_CELLS_PER_AVATAR': 2,
    'TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR': 0,
    'SCORE_DESPAWN_CHANCE': 0,
    'TARGET_NUM_PICKUPS_PER_AVATAR': 0,
    'PICKUP_SPAWN_CHANCE': 0,
    'NO_FOG_OF_WAR_DISTANCE': 1000,
    'PARTIAL_FOG_OF_WAR_DISTANCE': 1000,
    'GENERATOR': 'Level1',
    'START_HEIGHT': 5,
    'START_WIDTH': 1
}

class RequestMock(object):
    def __init__(self, num_games):
        self.value = self._generate_response(num_games)
        self.urls_requested = []

    def _generate_response(self, num_games):
        return {
            str(i): {
                'name': 'Level %s' % i,
                'settings': pickle.dumps(DEFAULT_LEVEL_SETTINGS)
            } for i in xrange(num_games)
        }

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)

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
                os.system("minikube stop")
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
                os.system("minikube stop")
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
        class GameCreatorRunner(Runner):
            def apply(self, received):
                mocker = RequestMock(1)
                with HTTMock(mocker):
                    ans = requests.get(self.binder._SERVER_URL + received)
                    self.binder.assertEqual(len(mocker.urls_requested), 1)
                    self.binder.assertEqual("/players/api/games/" in mocker.urls_requested[0], True)
                    return ans.text

        class GameRunner(Runner):
            def apply(self, received):
                mocker = RequestMock(1)
                with HTTMock(mocker):
                    ans = requests.get(self.binder._SERVER_URL + received)
                    self.binder.assertEqual(len(mocker.urls_requested), 1)
                    self.binder.assertEqual("/players/api/games/0/" in mocker.urls_requested[0], True)

                    return ans.text

        self.__build_test([
            (GameCreatorRunner(self), 1),
            (GameRunner(self), 1)
        ], True)



from unittest import TestSuite
from unittest import TextTestRunner

if __name__ == "__main__":
    suite = TestSuite()

    # suite.addTest(TestService("test_killing_creator_kills_game"))
    suite.addTest(TestService("test_games_get_generated"))

    runner = TextTestRunner()
    runner.run(suite)
