import time
import requests
import os


def delete_old_database():
    try:
        os.remove("../example_project/example_project/db.sqlite3")
        print("Database file in example_project DELETED!")
    except OSError:
        print("No database file found.")
        pass


def obtain_csrftoken(session):
    """
    A CSRF cookie token is required in order to not get a 403 Forbidden response by
    the post to the inputs.
    :return: String representing the token.
    """

    return session.cookies['csrftoken']


def create_session():
    """
    A integration test utility to create a browser session request for a single test.
    :return: A session object for requests.
    """

    return requests.Session()


def send_get_request(session, url):
    """
    Attempts to send a GET request up to 20 times (20s) if a RequestException is received
    back.

    :param session: Object representing the browser session.
    :param url: String, containing 'http://', with the URL of the target URL.
    :return: Response of GET.
    """
    fail_count = 0
    response = None

    while fail_count < 20:
        print("Attempting a GET request for the provided URL...")
        try:
            response = session.get(url)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            # Waits a second between the next attempt.
            print(e)
            time.sleep(1)
            fail_count += 1
            pass

    return response


def send_post_request(session, url, data):
    """
    Attempts to send a POST request up to 20 times (20s) if a RequestException is received
    back. NOTE: data must contain a CSRF token to authenticate the POST.

    :return: Response of POST.
    """
    fail_count = 0
    response = None

    while fail_count < 20:
        print("Attempting a GET request for the provided URL...")
        try:
            response = session.post(url, data=data)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            # Waits a second between the next attempt.
            print(e)
            time.sleep(1)
            fail_count += 1
            pass

    return response
