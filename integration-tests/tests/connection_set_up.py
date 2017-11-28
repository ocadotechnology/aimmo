import time
import requests
import os
import logging


logging.basicConfig(level=logging.WARNING)


def delete_old_database():
    try:
        os.remove("../example_project/example_project/db.sqlite3")
        logging.debug("Database file in example_project DELETED!")
    except OSError:
        logging.debug("No database file found.")
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
    Attempts to send a GET to the url. Server is already up as the test should
    be calling the `is_server_healthy()` function before calling this.

    :param session: Object representing the browser session.
    :param url: String, containing 'http://', with the URL of the target URL.
    :return: Response of GET.
    """
    response = None

    logging.debug("Attempting a GET request for the provided URL...")
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.debug(e)

    return response


def send_post_request(session, url, data):
    """
    Attempts to send a POST to the url. Server is already up as the test should
    be calling the `is_server_healthy()` function before calling this.

    :return: Response of POST.
    """
    response = None

    logging.debug("Attempting a POST request for the provided URL...")

    try:
        response = session.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.debug(e)

    return response


def is_server_healthy(url):
    """
    Function will only return True when the param URL returns a 2xx code. After
    45 seconds, the check assumes a timeout.
    :param url: http URL for the address to poll.
    :return: boolean value to indicate result.
    """

    attempts = 0

    logging.debug("Checking if the server is healthy...")
    while attempts <= 45:
        try:
            status_code = requests.get(url).status_code
            if int(str(status_code)[0]) == 2:
                return True
        except requests.exceptions.RequestException as e:
            pass

        attempts += 1
        time.sleep(1)

    return False
