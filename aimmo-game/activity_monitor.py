import asyncio
import logging
import time
from enum import Enum

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StatusOptions(Enum):
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3


class ActivityMonitor:
    def __init__(self):
        self.active_users = 0
        self.timer_running = True
        self.timer = Timer(callback=self.callback)
        self.status = StatusOptions.RUNNING

    def start_timer(self):
        if not self.timer_running:
            self.timer = Timer(callback=self.callback)
            self.timer_running = True

    def stop_timer(self):
        if self.timer_running:
            self.timer.cancel()
            self.timer_running = False

    async def callback(self):
        LOGGER.info("GAME MARKED AS INACTIVE, IT SHOULD NOW SHUTDOWN!")
        self.status = StatusOptions.STOPPED


async def default_callback():
    await asyncio.sleep(0.1)
    LOGGER.info("GAME MARKED AS INACTIVE, IT SHOULD NOW SHUTDOWN!")
    # telling thing to delete game should go here


class Timer:
    def __init__(self, timeout=3600, callback=default_callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()
