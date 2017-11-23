import traceback
import signal
import time
import os
import requests
import subprocess

URL = 'http://localhost:8000/players/accounts/login/'

try:
    try:
        os.remove("../example_project/example_project/db.sqlite3")
    except OSError:
        pass

    p = subprocess.Popen(["python", "../run.py"])

    session = requests.Session()
    failCount = 0

    while failCount < 20:
        try:
            response = session.get(URL)
            break
        except requests.exceptions.RequestException as e:
            time.sleep(1)
            failCount += 1
            pass

    # Retrieve the CSRF token first
    if 'csrftoken' in session.cookies:
        # Django 1.6 and up
        csrftoken = session.cookies['csrftoken']
    else:
        # older versions
        csrftoken = session.cookies['csrf']

    login_info = {
        'username': 'admin',
        'password': 'admin',
        'csrfmiddlewaretoken': csrftoken,
    }

    result_post = session.post(URL, data=login_info, headers=dict(Referer=URL))

except Exception as err:
    traceback.print_exc()
    raise
finally:
    os.killpg(0, signal.SIGTERM)
    time.sleep(0.9)
    os.killpg(0, signal.SIGKILL)
