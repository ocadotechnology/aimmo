import requests


class Communicator(object):
    """
    This class encapsulates the communication between aimmo-game
    and the django server
    """
    def __init__(self, api_url, completion_url):
        self.api_url = api_url
        self.completion_url = completion_url

    def get_game_metadata(self):
        return requests.get(self.api_url).json()

    def mark_game_complete(self, data=None):
        return requests.post(requests.post(self.completion_url, json=data))
