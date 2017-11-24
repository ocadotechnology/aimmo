import os
import signal
import time
import subprocess
from unittest import TestCase

from connection_set_up import (create_session, send_get_request, send_post_request,
                               obtain_csrftoken, delete_old_database)


class TestIntegration(TestCase):
    def test_default(self):
        """
        A test that will run on a clean & empty database, create all migrations, new
        browser session and passes a CSRF token with the POST input request.
        
        Server gets killed at the end of the test.
        """
        url = 'http://localhost:8000/players/accounts/login/'

        delete_old_database()

        subprocess.Popen(["python",  "../run.py"], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        time.sleep(15)

        print("Creating session...")
        session = create_session()

        print ("Starting GET request loop...")
        get_response = send_get_request(session, url)

        print("Obtaining CSRF Token...")
        csrftoken = obtain_csrftoken(session)

        login_info = {
            'username': 'admin',
            'password': 'admin',
            'csrfmiddlewaretoken': csrftoken,
        }

        print("Sending post response...")

        send_post_request(session, url, login_info)

        os.killpg(0, signal.SIGTERM)
        time.sleep(0.9)
        os.killpg(0, signal.SIGKILL)
