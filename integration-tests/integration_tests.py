import traceback

import signal

import time

import os
import requests
import subprocess
from lxml import html


try:
    print("start")
    try:
        os.remove("../example_project/example_project/db.sqlite3")
    except:
        pass
    print("db removed")

    p = subprocess.Popen(["python", "../run.py"])

    print("os system call")

    session = requests.Session()

    while True:
        try:
            response = session.get('http://localhost:8000')
            break
        except:
            time.sleep(1)
            pass

    print("session created, print next")

    print(response)

    # Instead of the below, remove 'django.middleware.csrf.CsrfViewMiddleware' from MIDDLEWEARE in django settings JUST FOR THIS TEST!!!

    # result = session.get('http://localhost:8000/players/accounts/login/')
    # tree = html.fromstring(result.content)
    # token = tree.xpath('//input[@name="csrfmiddlewaretoken"]/@value')

    # print(token)

    login_info = {
        'username': 'admin',
        'password': 'admin',
        # 'csrfmiddlewaretoken': token,
    }

    result_post = session.post('http://localhost:8000/players/accounts/login/', data=login_info)

    print(result_post)

except Exception as err:
    traceback.print_exc()
    raise
finally:
    os.killpg(0, signal.SIGTERM)
    time.sleep(0.9)
    os.killpg(0, signal.SIGKILL)
