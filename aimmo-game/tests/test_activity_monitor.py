import asyncio
import time

import pytest
from activity_monitor import ActivityMonitor, Timer
from asynctest import CoroutineMock


@pytest.fixture
def activity_monitor():
    activity_monitor = ActivityMonitor()
    activity_monitor.callback = CoroutineMock()
    return activity_monitor


@pytest.fixture
def event_loop():
    return asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_timer_stops_correctly(activity_monitor, event_loop):
    assert activity_monitor.active_users == 0
    assert not activity_monitor.timer.cancelled()

    activity_monitor.active_users = 1
    await asyncio.sleep(0.00001)

    assert activity_monitor.active_users == 1
    assert activity_monitor.timer.cancelled()


@pytest.mark.asyncio
async def test_timer_starts_correctly(activity_monitor, event_loop):
    activity_monitor.active_users = 2
    await asyncio.sleep(0.00001)

    assert activity_monitor.active_users == 2
    assert activity_monitor.timer.cancelled()

    activity_monitor.active_users = 0
    await asyncio.sleep(0.00001)

    assert activity_monitor.active_users == 0
    assert not activity_monitor.timer.cancelled()


@pytest.mark.asyncio
async def test_callback_called_when_timer_expires(activity_monitor):
    assert activity_monitor.active_users == 0
    assert not activity_monitor.timer.cancelled()

    activity_monitor.timer = Timer(timeout=0, callback=activity_monitor.callback)
    await asyncio.sleep(0.00001)

    activity_monitor.callback.assert_called()
