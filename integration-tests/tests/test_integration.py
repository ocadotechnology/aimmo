import os
import signal
import time
import subprocess
import logging
from unittest import TestCase

from connection_set_up import (create_session, send_get_request, send_post_request,
                               obtain_csrftoken, delete_old_database, is_server_healthy)

logging.basicConfig(level=logging.WARNING)


class TestIntegration(TestCase):
    def test_superuser_authentication(self):
        """
        A test that will run on a clean & empty database, create all migrations, new
        browser session and passes a CSRF token with the POST input request.
        
        Server gets killed at the end of the test.
        """
        url = 'http://localhost:8000/players/accounts/login/'

        delete_old_database()

        p = subprocess.Popen(["python",  "../run.py"], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

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

        os.kill(int(p.pid), signal.SIGKILL)
