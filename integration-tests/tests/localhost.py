from __future__ import absolute_import

from unittest import TestCase

import os
import subprocess
import time
import signal

# TODO: install test globally

import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../../')

import importlib
mockery = importlib.import_module("aimmo-game-creator.tests.test_worker_manager")

# def kill_service():
#     os.killpg(0, signal.SIGTERM)
#     time.sleep(1)
#     time.sleep(1)
#     os.killpg(0, signal.SIGKILL)

def run_command_async(args):
    p = subprocess.Popen(args)
    return p

class TestService(TestCase):
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'aimmo-game-creator', 'service.py')

    def __setup_environment(self):
        os.environ['AIMMO_MODE'] = 'threads'
        os.environ['WORKER_MANAGER'] = 'local'
        os.environ['GAME_API_URL'] = 'http://test/games'

        self._SERVER_URL = 'http://test/'
        self._SERVER_PORT = '5000'

    def setUp(self):
        self.__setup_resources()
        self.__setup_environment()

    def test_killing_creator_kills_game(self):
        try:
            game = run_command_async(['python', self._SERVICE_PY, self._SERVER_URL, self._SERVER_PORT])
        finally:
            os.kill(game.pid, signal.SIGKILL)

    def test_games_get_generated(self):
        try:
            game = run_command_async(['python', self._SERVICE_PY, self._SERVER_URL, self._SERVER_PORT])
            mocker = mockery.RequestMock(0)
        finally:
            os.kill(game.pid, signal.SIGKILL)

from unittest import TestSuite
from unittest import TextTestRunner

if __name__ == "__main__":
    suite = TestSuite()

    suite.addTest(TestService("test_killing_creator_kills_game"))
    suite.addTest(TestService("test_games_get_generated"))

    runner = TextTestRunner()
    runner.run(suite)
