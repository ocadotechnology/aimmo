import os
import signal
import time
import subprocess
from connection_set_up import (create_session, send_get_request, send_post_request,
                               obtain_csrftoken, delete_old_database)

URL = 'http://localhost:8000/players/accounts/login/'

delete_old_database()

p = subprocess.Popen(["python",  "../run.py"])
time.sleep(15)

print("Creating session")
session = create_session()

print ("Starting GET request loop")
get_response = send_get_request(session, URL)

print("Obtaining CSRF Token.")
csrftoken = obtain_csrftoken(session)

login_info = {
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrftoken,
}

print("Sending post response")

post_response = send_post_request(session, URL, login_info)

os.killpg(0, signal.SIGTERM)
time.sleep(0.9)
os.killpg(0, signal.SIGKILL)
