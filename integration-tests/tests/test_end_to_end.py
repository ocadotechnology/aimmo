from __future__ import absolute_import

from unittest import TestCase, skipUnless, skip
import requests

import os
import time
import signal
import subprocess
import sys
import json
sys.path.append('../../')
FNULL = open(os.devnull, 'w')

import logging
import traceback

from misc import run_command_async, kill_process_tree

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

    def __start_django(self, kubernates=False):
        print(self._SERVICE_PY)
        if not kubernates:
            self.django = run_command_async(["python", self._SERVICE_PY], self._SCRIPT_LOCATION, verbose=self._VERBOSE)
        else:
            self.django = run_command_async(["python", self._SERVICE_PY, "-k"], self._SCRIPT_LOCATION, verbose=self._VERBOSE)
        self.session = requests.Session()

    def __cleanup(self, kubernates=False):
        print("Terminating processes....")
        time.sleep(1)
        try:
            if not kubernates:
                kill_process_tree(self.django.pid)
            else:
                print("WTF")
                os.system("minikube delete")
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

    def __pool_callback(self, callback, tries):
        while tries > 0:
            tries -= 1
            time.sleep(1)
            try:
                if callback():
                    return
                    break
            except:
                print("Waiting for resource...")
        self.assertTrue(False)

    def start_django(self, kubernates):
        try:
            self.__start_django(kubernates)
        finally:
            self.__cleanup()

    def __find_game_id_by_name(self, name):
        # getting the games list
        games = json.loads(self.__get_resource("players/api/games", 200).text)

        # getting the level list
        level_list = list(filter(lambda (x, y): name in y["name"], list(games.items())))
        self.assertEqual(len(level_list), 1)
        level_id = list(x for x,y in level_list)[0]

        return level_id

    def __check_redirect(self, resource):
        login_redirect_page = self.__get_resource(resource, 200).text
        login_form_template = """<form method="post" action="/django.contrib.auth/login/">"""
        self.assertTrue(login_form_template in login_redirect_page)

    @skip("Problem with finding game by name.")
    def level_1(self, kubernates):
        try:
            self.__start_django(kubernates)

            self.__pool_callback(callback=lambda: self.__get_resource("", 200).status_code == 200, tries=30)
            self.__get_resource("players", 200)

            # getting the first level
            self.__pool_callback(callback=lambda: self.__find_game_id_by_name("Level 1") != None, tries=30)
            level1_id = self.__find_game_id_by_name("Level 1")

            # trying to program, getting to login page
            self.__check_redirect("players/program_level/" + level1_id)

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
            self.__pool_callback(callback=lambda: "HEALTHY" in self.session.get(host).text, tries=30)
        except Exception as e:
            logging.error(traceback.format_exc())
        finally:
            self.__cleanup()

    @skip("Problem with finding game by name.")
    def cant_code_without_login(self, kubernates):
        try:
            self.__start_django(kubernates)

            self.__pool_callback(callback=lambda: self.__get_resource("", 200).status_code == 200, tries=30)

            # getting the first level
            self.__pool_callback(callback=lambda: self.__find_game_id_by_name("Level 1") != None, tries=30)
            level1_id = self.__find_game_id_by_name("Level 1")

            # trying to program, getting to login page
            self.__check_redirect("players/program_level/" + level1_id)

            # posting login data
            self.__post_resouce("django.contrib.auth/login/", 200, {
                'username':'batman',
                'password':'batman'})

            # trying to program, getting to login page
            self.__check_redirect("players/program_level/" + level1_id)
        finally:
            self.__cleanup()

    def test_local_start_django(self): self.start_django(kubernates=False)
    def test_local_level_1(self): self.level_1(kubernates=False)
    def test_local_cant_code_without_login(self): self.cant_code_without_login(kubernates=False)

    @skipUnless('RUN_KUBE_TESTS' in os.environ, "See setup.py.")
    def test_kube_start_django(self): self.start_django(kubernates=True)

    @skipUnless('RUN_KUBE_TESTS' in os.environ, "See setup.py.")
    def test_kube_level_1(self): self.level_1(kubernates=True)

    @skipUnless('RUN_KUBE_TESTS' in os.environ, "See setup.py.")
    def test_kube_cant_code_without_login(self):  self.cant_code_without_login(kubernates=True)
