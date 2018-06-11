import os
import signal
import time
import subprocess
import logging
import unittest
from django.test.client import Client
import psutil
from aimmo_runner import runner
from connection_api import (create_session, send_get_request, send_post_request,
                            obtain_csrftoken, delete_old_database, is_server_healthy)
from django.conf import settings
from django.core.urlresolvers import reverse
import time
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

    def test_superuser_authentication(self):
        """
        A test that will run on a clean & empty database, create all migrations, new
        browser session and passes a CSRF token with the POST input request.
        
        Server gets killed at the end of the test.
        """
        time.sleep(5)
        import django
        django.setup()
        from django.test.utils import setup_test_environment
        setup_test_environment()
        url_string = 'aimmo/login'
        print "INSIDE TEST CASE"
        delete_old_database()

        os.chdir(runner.ROOT_DIR_LOCATION)
        self.processes = runner.run_something(use_minikube=False, server_wait=False, capture_output=True, test_env=True)

        #self.assertTrue(is_server_healthy(url_string))

        logging.debug("Creating session...")
        #session = create_session()
        print "CREATING CLIENT"
        url = 'http://localhost:8000/players/accounts/login/'
        #send_get_request(session, url)

        client = Client()
        print reverse(url_string)
        response = client.get(reverse(url_string))
        logging.debug("Obtaining CSRF Token...")
        # csrftoken = obtain_csrftoken(Client().session)
        print "GETTING TOKEN    "
        print isinstance(response.context, type(None))
        csrf_token = response.context['csrf_token']
        login_info = {
            'username': 'admin',
            'password': 'admin',
            'csrftoken': csrf_token,
        }

        logging.debug("Sending post response...")

        print "SENDING POST REQUEST"
        response = client.post(url, login_info)
        print response
        #response = send_post_request(session, url, login_info)
        self.assertEquals(response.status_code, 302)
