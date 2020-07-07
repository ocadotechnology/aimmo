import aiohttp
import os


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

    async def get_game_metadata(self):
        try:
            async with self.session.get(f"{self.django_api_url}users/") as response:
                if response.status == 200:
                    return await response.read()
                else:
                    pass
        except (aiohttp.ClientConnectionError, aiohttp.ContentTypeError):
            pass

    async def patch_token(self, data):
        response = await self.session.patch(
            self.token_url, headers={"Game-token": os.environ["TOKEN"]}, json=data
        )
        return response

    async def patch_game(self, data):
        response = await self.session.patch(
            self.django_api_url, headers={"Game-token": os.environ["TOKEN"]}, json=data
        )
        return response

    async def close_session(self, app):
        await self.session.close()
