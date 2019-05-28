import os

import aiohttp
import requests


class DjangoCommunicator(object):
    """
    This class encapsulates the communication between aimmo-game
    and the django server
    """

    def __init__(self, django_api_url, completion_url):
        self.session = aiohttp.ClientSession()
        self.django_api_url = django_api_url
        self.completion_url = completion_url
        self.token_url = self.django_api_url + "token/"

    def get_game_metadata(self):
        return requests.get(self.django_api_url).json()

    def mark_game_complete(self, data=None):
        return requests.post(requests.post(self.completion_url, json=data))

    async def patch_token(self, data):
        response = await self.session.patch(
            self.token_url, headers={"Game-token": os.environ["TOKEN"]}, json=data
        )
        return response

    async def patch_game(self, data):
        response = await self.session.patch(
            self.token_url, headers={"Game-token": os.environ["TOKEN"]}, json=data
        )
        return response

    def close_session(self, app):
        self.session.close()
