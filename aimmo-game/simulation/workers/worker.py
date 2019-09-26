import logging
from asyncio import CancelledError

from aiohttp import ClientSession, ClientResponseError, ServerDisconnectedError

LOGGER = logging.getLogger(__name__)


class Worker(object):
    def __init__(self, player_id, game_port):
        self.log = None
        self.player_id = player_id
        self.game_port = game_port
        self.code = None
        self.serialized_action = None
        self.has_code_updated = False
        self.url = self._create_worker()
        self.ready = False

    def _set_defaults(self):
        self.log = None
        self.serialized_action = None
        self.has_code_updated = False

    def _create_worker(self):
        raise NotImplementedError

    def remove_worker(self):
        raise NotImplementedError

    async def fetch_data(self, state_view):
        if self.code is None:
            self._set_defaults()
            return
        try:
            async with ClientSession(raise_for_status=True) as session:
                code_and_options = {"code": self.code, "options": {}, "state": None}
                data = {**state_view, **code_and_options}
                response = await session.post(f"{self.url}/turn/", json=data)
                data = await response.json()
                self.serialized_action = data["action"]
                self.log = data["log"]
                self.has_code_updated = data["avatar_updated"]
                self.ready = True
        except (ClientResponseError, ServerDisconnectedError):
            LOGGER.info("Could not connect to worker, probably not ready yet")
            self._set_defaults()
        except CancelledError as e:
            LOGGER.error("Worker took too long to respond: {}".format(e))
            self._set_defaults()
        except KeyError as e:
            LOGGER.error("Missing key in data from worker: {}".format(e))
            self._set_defaults()
        except Exception as e:
            LOGGER.exception("Unknown error while fetching turn data.")
            LOGGER.exception(e)
            self._set_defaults()
