from __future__ import absolute_import

from unittest import TestCase, skip
import requests
from simulation import SnapshotProcessor

import os
import time
import json
import logging

FNULL = open(os.devnull, 'w')


from misc import run_command_async
from misc import kill_process_tree
from misc import get_ip

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
REQUEST_LOG = logging.getLogger("request-log")
REQUEST_LOG.setLevel(logging.DEBUG)


class TestService(TestCase):
    """
        This is an end-to-end test case. We test 3 scenarios:
        1. Simple server start-up
        2. Try to use the service with wrong credentials
        3. Try to play the first level with a default created character

        As most of the functionality is accessible using the api or other
        methods, we use simple requests rather than Selenium (though
        selenium should be easily be added to the module).

        Resources are exposed at plain paths inside aimmo-game/service.
        We can also use minikube with this test, but we need a different
        nginx configuration for this.

        Use verbose=True to see the server logs for localhost.
    """
    def __setup_resources(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..'))
        self._SERVICE_PY = os.path.join(self._SCRIPT_LOCATION, 'run.py')
        self._CODE = 'class Avatar: pass'

    def __setup_environment(self):
        self._VERBOSE = False

        self._SERVER_URL = 'http://' + get_ip() + ':8000/'
        self._SERVER_PORT = '8000'

    def __start_django(self, kube):
        if not kube:
            self.django = run_command_async(["python", self._SERVICE_PY], self._SCRIPT_LOCATION, verbose=self._VERBOSE)
        else:
            self.django = run_command_async(["python", self._SERVICE_PY, "-k"], self._SCRIPT_LOCATION, verbose=self._VERBOSE)
        self.session = requests.Session()

    def __cleanup(self, kube):
        LOGGER.info("Terminating processes....")
        time.sleep(1)
        try:
            if not kube:
                kill_process_tree(self.django.pid)
            else:
                LOGGER.info("Stopping minikube...")
                os.system("minikube stop")
                kill_process_tree(self.django.pid)
        finally:
            self.session = None

    def __get_resource(self, resource, code, host=None):
        if host is None:
            host = self._SERVER_URL

        url = host + resource
        REQUEST_LOG.info("getting: " + url)

        result = self.session.get(url)

        # asserting the response
        self.assertEqual(result.status_code, code)
        return result

    def __post_resource(self, resource, code, payload):
        url = self._SERVER_URL + resource
        REQUEST_LOG.info("posting: " + url)

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
                LOGGER.info("Waiting for resource...")
        self.assertTrue(False)

    def start_django(self, kube):
        try:
            self.__start_django(kube)
        finally:
            self.__cleanup(kube)

    def __find_game_id_by_name(self, name):
        # getting the games list
        response = self.__get_resource("players/api/games/", 200).text
        games = json.loads(response)

        # getting the level list
        level_list = list(filter(lambda (x, y): name in y["name"], list(games.items())))
        self.assertEqual(len(level_list), 1)
        level_id = list(x for x,y in level_list)[0]

        return level_id

    def __check_redirect(self, resource):
        login_redirect_page = self.__get_resource(resource, 200).text
        login_form_template = """<form method="post" action="/django.contrib.auth/login/">"""
        self.assertTrue(login_form_template in login_redirect_page)

    def level_1(self, kube):
        try:
            self.__start_django(kube)
            if kube:
                LOGGER.info("Waiting for minikube to start...")
                time.sleep(300)

            self.__pool_callback(callback=lambda: self.__get_resource("", 200).status_code == 200, tries=30)

            # trying to program, getting to login page
            self.__check_redirect("players/program_level/1")

            # posting login data
            self.__post_resource("django.contrib.auth/login/", 200, {
                'username':'admin',
                'password':'admin'})

            # Check code and watch pages; this also may add the level to DB
            code_page = self.__get_resource("players/program_level/1", 200).text
            watch_page = self.__get_resource("players/watch_level/1", 200).text

            # Check the level has been added
            self.__pool_callback(callback=lambda: self.__find_game_id_by_name("Level 1") != None, tries=30)
            level1_id = self.__find_game_id_by_name("Level 1")

            # Check the level pages by level id
            code_page = self.__get_resource("players/program/" + level1_id, 200).text
            watch_page = self.__get_resource("players/watch/" + level1_id, 200).text

            host, path = self.__get_socketio_info(watch_page)
            LOGGER.info("HOST:" + host)

            # This adds the code to the database
            self.__get_resource("players/api/code/1", 200)

            if not kube:
                self.__pool_callback(callback=lambda: "HEALTHY" in self.session.get(host + "/").text, tries=30)

            self.assertEqual(self.__get_resource("/plain/1/connect", 200, host).text, "CONNECT")
            self.assertEqual(self.__get_resource("/plain/1/client-ready", 200, host).text, "RECEIVED USER READY 1")

            processor = SnapshotProcessor(self)
            snapshots = 100

            while snapshots > 0:
                # getting the world_state
                world_state = self.__get_resource("/plain/1/update", 200, host).text

                # send the snapshot to the processor
                # the processor will track and verify the information
                processor.receive_snapshot(world_state)

                time.sleep(0.1)
                snapshots -= 1

            # if the user was not added to the test, then something is probably wrong
            processor.check_player_added()

            self.assertEqual(self.__get_resource("/plain/1/exit-game", 200, host).text, "EXITING GAME FOR USER 1")
        finally:
            self.__cleanup(kube)

    def cant_code_without_login(self, kube):
        try:
            self.__start_django(kube)

            self.__pool_callback(callback=lambda: self.__get_resource("", 200).status_code == 200, tries=30)

            # trying to program, getting to login page
            self.__check_redirect("players/program_level/1")

            # posting login data
            self.__post_resource("django.contrib.auth/login/", 200, {
                'username':'batman',
                'password':'batman'})

            # trying to program, getting to login page
            self.__check_redirect("players/program_level/1")
        finally:
            self.__cleanup(kube)

    def test_local_start_django(self): self.start_django(kube=False)

    def test_local_level_1(self): self.level_1(kube=False)

    def test_local_cant_code_without_login(self): self.cant_code_without_login(kube=False)

    @skip("The nginx proxy does not expose the plain resources.")
    def test_kube_level_1(self): self.level_1(kube=True)
