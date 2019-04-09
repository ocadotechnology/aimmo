import asyncio
import time
from enum import Enum


class StatusOptions(Enum):
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3


class ActivityMonitor:
    def __init__(self):
        self.status_options = StatusOptions

        self.active_users = 0
        self._status = self.status_options.RUNNING

        self.timer_running = False
        self.timer = None
        self.start_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer = asyncio.ensure_future(asyncio.sleep(3600))

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.timer.cancel()

    async def check_active_users(self):
        if not self.active_users:
            await self.start_timer()
        else:
            self.stop_timer()

    async def timer_completed(self):
        try:
            await self.timer
            self._status = self.status_options.STOPPED
        except asyncio.CancelledError:
            # CancelledError occurs if the future/task was cancelled before being awaited
            pass

    def get_status(self) -> StatusOptions:
        return self._status

    def update_active_users(self, value: int):
        self.active_users = value
