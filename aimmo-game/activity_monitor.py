"""
Module for keeping track of inactivity for a given game.
"""

import asyncio
import logging
import os
import time
from enum import Enum
from types import CoroutineType

import aiohttp

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SECONDS_TILL_CONSIDERED_INACTIVE = 10


class StatusOptions(Enum):
    RUNNING = "r"
    PAUSED = "p"
    STOPPED = "s"

    def __str__(self):
        return self.value


class ActivityMonitor:
    """
    Keeps track of the number of users currently connected.

    If no users are connected (measured by sockets) after a certain length
    of time, the game is marked as stopped and the pods will be shut down shortly after
    """

    def __init__(self,):
        self.__active_users = 0
        self.timer = Timer(SECONDS_TILL_CONSIDERED_INACTIVE, self.change_status_to_stopped)
        self.active_users = 0

    def _start_timer(self):
        if not self.timer.is_running:
            self.timer = Timer(SECONDS_TILL_CONSIDERED_INACTIVE, self.change_status_to_stopped)
            self.timer.is_running = True

    def _stop_timer(self):
        if self.timer.is_running:
            self.timer.cancel()
            self.timer.is_running = False

    @property
    def active_users(self):
        return self.__active_users

    @active_users.setter
    def active_users(self, value: float):
        self.__active_users = value
        if self.__active_users:
            self._stop_timer()
        else:
            self._start_timer()

    async def change_status_to_stopped(self):
        LOGGER.info("Timer expired! Marking game as STOPPED")
        api_url = os.environ.get(
            "GAME_API_URL", "http://localhost:8000/aimmo/api/games/"
        )
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                api_url,
                data={"status": StatusOptions.STOPPED},
                headers={"Game-token": os.environ["TOKEN"]},
            ) as response:
                print(response)

        return None


class Timer:
    """
    Generic Timer with callback.

    This sleeps for `timeout=X` seconds, after X seconds the
    callback function is called, this happens asynchronously.
    """

    def __init__(self, timeout: float, callback: CoroutineType):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())
        self.is_running = True

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()
