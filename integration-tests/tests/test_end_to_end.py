from __future__ import absolute_import

from unittest import TestCase
import requests

from socketio_client import SocketClient

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
    """
        Use verbose=True to see the server logs for localhost.
    """
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'run.py')
        self._CODE = 'class Avatar: pass'

    def __setup_environment(self):
        self._VERBOSE = False

        os.environ['AIMMO_MODE'] = 'threads'
        os.environ['WORKER_MANAGER'] = 'local'
        os.environ['GAME_API_URL'] = 'http://localhost:8000/players/api/games/'

        self._SERVER_URL = 'http://localhost:8000/'
        self._SERVER_PORT = '8000'

    def __start_scoketio(self, host_port, path):
        host = host_port.split(":")[0] + ":" + host_port.split(":")[1]
        port = host_port.split(':')[2]

        self.socket_io = SocketClient(str(host), int(port), path, self)
        self.socket_io.start()

    def __start_django(self):
        print(self._SERVICE_PY)
        self.django = run_command_async(["python", self._SERVICE_PY], self._SCRIPT_LOCATION, verbose=self._VERBOSE)
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

    def __get_socketio_info(self, page):
        def lookup(string):
            return list(filter(lambda x: string in x, page.split('\n')))[0].split('"')[1]
        return lookup("GAME_URL_BASE"), lookup("GAME_URL_PATH")

    def setUp(self):
        self.__setup_resources()
        self.__setup_environment()

    # def test_start_django(self):
    #     try:
    #         self.__start_django()
    #     finally:
    #         self.__cleanup()

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
            code_page = self.__get_resource("players/program_level/" + level1_id, 200).text

            # check we can watch the game
            watch_page = self.__get_resource("players/watch_level/" + level1_id, 200).text
            host, path = self.__get_socketio_info(watch_page)

            # wait for 30 seconds for pods to start
            tries = 30
            while tries > 0:
                time.sleep(1)
                try:
                    if "HEALTHY" in self.session.get(host).text:
                        print "Workers started..."
                        break
                except:
                    print("Waiting for game...")
            self.assertTrue(tries > 0)

            time.sleep(5)
            # Starting the socket io test part
            self.__start_scoketio(host, path)
        finally:
            self.__cleanup()
