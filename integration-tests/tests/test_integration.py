import os
import signal
import time
import subprocess
import logging
import unittest

import psutil
from aimmo_runner import runner
from connection_api import (create_session, send_get_request, send_post_request,
                            obtain_csrftoken, delete_old_database, is_server_healthy)

logging.basicConfig(level=logging.WARNING)


class TestIntegration(unittest.TestCase):

    def tearDown(self):
        """
        Kills the process and its children peacefully.
        """
        print(self.processes)

        for process in self.processes:
            print(process)
            try:
                parent = psutil.Process(process.pid)
            except psutil.NoSuchProcess:
                return

            children = parent.children(recursive=True)

            for child in children:
                child.terminate()

            parent.terminate()

    def test_superuser_authentication(self):
        """
        A test that will run on a clean & empty database, create all migrations, new
        browser session and passes a CSRF token with the POST input request.
        
        Server gets killed at the end of the test.
        """
        url = 'http://localhost:8000/players/accounts/login/'

        delete_old_database()

        os.chdir(runner.ROOT_DIR_LOCATION)
        self.processes = runner.run(use_minikube=False, server_wait=False)

        self.assertTrue(is_server_healthy(url))

        logging.debug("Creating session...")
        session = create_session()

        send_get_request(session, url)

        logging.debug("Obtaining CSRF Token...")
        csrftoken = obtain_csrftoken(session)

        login_info = {
            'username': 'admin',
            'password': 'admin',
            'csrfmiddlewaretoken': csrftoken,
        }

        logging.debug("Sending post response...")

        response = send_post_request(session, url, login_info)
        self.assertEquals(response.status_code, 200)
