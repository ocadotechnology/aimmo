import aiohttp
import os
from asyncio import TimeoutError


class DjangoCommunicator(object):
    """
    This class encapsulates the communication between aimmo-game
    and the django server
    """

    def __init__(self, django_api_url):
        timeout = aiohttp.ClientTimeout(total=1)
        self.session = aiohttp.ClientSession(timeout=timeout)
        self.django_api_url = django_api_url
        self.token_url = self.django_api_url + "token/"

    async def get_game_metadata(self):
        try:
            async with self.session.get(f"{self.django_api_url}users/") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise GameMetadataFetchFailedError
        except (aiohttp.ClientConnectionError, aiohttp.ContentTypeError, TimeoutError):
            raise GameMetadataFetchFailedError

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


class GameMetadataFetchFailedError(Exception):
    pass
