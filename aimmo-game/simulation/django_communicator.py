import requests


class DjangoCommunicator(object):
    """
    This class encapsulates the communication between aimmo-game
    and the django server
    """
    def __init__(self, django_api_url, completion_url):
        self.django_api_url = django_api_url
        self.completion_url = completion_url

    def get_game_metadata(self):
        return requests.get(self.django_api_url).json()

    def mark_game_complete(self, data=None):
        return requests.post(requests.post(self.completion_url, json=data))
