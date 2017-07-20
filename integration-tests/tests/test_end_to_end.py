from __future__ import absolute_import

from unittest import TestCase

import os
import signal
import subprocess
import sys
sys.path.append('../../')
FNULL = open(os.devnull, 'w')

def run_command_async(args, cwd="."):
    p = subprocess.Popen(args, cwd=cwd, stdout=FNULL, stderr=subprocess.STDOUT)
    return p

class TestService(TestCase):
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'run.py')

    def __setup_environment(self):
        os.environ['AIMMO_MODE'] = 'threads'
        os.environ['WORKER_MANAGER'] = 'local'
        os.environ['GAME_API_URL'] = 'http://localhost:8000/players/api/games/'

        self._SERVER_URL = 'http://localhost:8000/'
        self._SERVER_PORT = '8000'

    def __start_django(self):
        self.django = run_command_async(["python", self._SERVICE_PY])

    def __cleanup(self):
        try:
            os.system("pkill -TERM -P " + str(self.django.pid))
            os.kill(self.django.pid, signal.SIGKILL)
        finally:
            pass

    def setUp(self):
        self.__setup_resources()
        self.__setup_environment()

    def test_start_django(self):
        try:
            self.__start_django()
        finally:
            self.__cleanup()

    def test_start_game(self):
        try:
            self.__start_django()
        finally:
            self.__cleanup()
