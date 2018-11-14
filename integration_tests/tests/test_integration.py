import os
import logging
import mock
import unittest
from django.test.client import Client
import psutil
from aimmo_runner import runner
from connection_api import (create_session, send_get_request, send_post_request,
                            obtain_csrftoken, delete_old_database, is_server_healthy)
from django.core.urlresolvers import reverse
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

    @mock.patch('docker.from_env')
    def test_superuser_authentication(self, docker_from_env):
        """
        A test that will run on a clean & empty database, create all migrations, new
        browser session and passes a CSRF token with the POST input request.
        
        Server gets killed at the end of the test.
        """
        url_string = 'aimmo/login'
        delete_old_database()

        os.chdir(runner.ROOT_DIR_LOCATION)
        self.processes = runner.run(use_minikube=False, server_wait=False, capture_output=True, test_env=True)
        client = Client()
        response = client.get(reverse(url_string))
        self.assertEqual(response.status_code, 200)
        csrf_token = response.context['csrf_token']

        login_info = {
            'username': 'admin',
            'password': 'admin',
            'csrftoken': csrf_token,
        }

        response = client.post(reverse(url_string), login_info)
        self.assertEqual(response.status_code, 302)
