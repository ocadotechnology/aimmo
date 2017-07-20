from __future__ import absolute_import

from unittest import TestCase
import requests

import os
import time
import signal
import subprocess
import sys
import json
sys.path.append('../../')
FNULL = open(os.devnull, 'w')

def run_command_async(args, cwd=".", verbose=False):
    if verbose:
        p = subprocess.Popen(args, cwd=cwd)
    else:
        p = subprocess.Popen(args, cwd=cwd, stdout=FNULL, stderr=subprocess.STDOUT)
    return p

class TestService(TestCase):
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'run.py')
        self._CODE = 'class Avatar: pass'

    def __setup_environment(self):
        os.environ['AIMMO_MODE'] = 'threads'
        os.environ['WORKER_MANAGER'] = 'local'
        os.environ['GAME_API_URL'] = 'http://localhost:8000/players/api/games/'

        self._SERVER_URL = 'http://localhost:8000/'
        self._SERVER_PORT = '8000'

    def __start_django(self):
        print(self._SERVICE_PY)
        self.django = run_command_async(["python", self._SERVICE_PY], self._SCRIPT_LOCATION)
        self.session = requests.Session()

    def __cleanup(self):
        try:
            time.sleep(1)
            os.system("pkill -TERM -P " + str(self.django.pid))
            os.kill(self.django.pid, signal.SIGKILL)
        finally:
            self.session = None

    def __get_resource(self, resource, code):
        url = self._SERVER_URL + resource
        print("> getting: " + url)

        result = self.session.get(url)

        # asserting the response
        self.assertEqual(result.status_code, code)
        return result

    def __post_resouce(self, resource, code, payload):
        url = self._SERVER_URL + resource
        print("> posting: " + url)

        # setting CSRF...
        payload['csrfmiddlewaretoken']=self.session.cookies['csrftoken']
        result = self.session.post(url, data=payload)

        # asserting the response
        self.assertEqual(result.status_code, code)
        return result

    def setUp(self):
        self.__setup_resources()
        self.__setup_environment()

    def test_start_django(self):
        try:
            self.__start_django()
        finally:
            self.__cleanup()

    def test_level_1(self):
        try:
            self.__start_django()

            self.__get_resource("", 200)
            self.__get_resource("players", 200)

            # getting the games list
            games = json.loads(self.__get_resource("players/api/games", 200).text)

            # getting the first level
            level1_list = list(filter(lambda (x, y): "Level 1" in y["name"], list(games.items())))
            self.assertEqual(len(level1_list), 1)
            level1_id = list(x for x,y in level1_list)[0]

            # trying to program, getting to login page
            login_redirect_page = self.__get_resource("players/program_level/" + level1_id, 200).text
            login_form_template = """<form method="post" action="/django.contrib.auth/login/">"""
            self.assertTrue(login_form_template in login_redirect_page)

            # posting login data
            self.__post_resouce("django.contrib.auth/login/", 200, {
                'username':'admin',
                'password':'admin'})

            # check the code is OK
            code_page = self.__get_resource("players/program_level/" + level1_id, 200)

            # check we can watch the game
            code_page = self.__get_resource("players/watch_level/" + level1_id, 200)
        finally:
            self.__cleanup()
