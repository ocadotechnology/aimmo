import logging
import os
import unittest

import mock
import psutil
from django.core.urlresolvers import reverse
from django.test.client import Client

from aimmo_runner import runner
from .connection_api import delete_old_database

logging.basicConfig(level=logging.WARNING)


class TestIntegration(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIntegration, self).__init__(*args, **kwargs)
        self.processes = []

    def tearDown(self):
        """
        Kills the process and its children peacefully.
        """

        for process in self.processes:
            try:
                parent = psutil.Process(process.pid)
            except psutil.NoSuchProcess:
                return

            children = parent.children(recursive=True)

            for child in children:
                child.terminate()

            parent.terminate()

    @mock.patch("docker.from_env")
    def test_superuser_authentication(self, docker_from_env):
        """
        A test that will run on a clean & empty database, create all migrations, new
        browser session and passes a CSRF token with the POST input request.
        
        Server gets killed at the end of the test.
        """
        url_string = "kurono/login"
        delete_old_database()

        os.chdir(runner.ROOT_DIR_LOCATION)
        self.processes = runner.run(
            use_minikube=False, server_wait=False, capture_output=True, test_env=True
        )
        client = Client()
        response = client.get(reverse(url_string))
        self.assertEqual(response.status_code, 200)
        csrf_token = response.context["csrf_token"]

        login_info = {"username": "admin", "password": "admin", "csrftoken": csrf_token}

        response = client.post(reverse(url_string), login_info)
        self.assertEqual(response.status_code, 302)
