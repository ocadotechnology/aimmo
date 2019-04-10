import asyncio
import time

import pytest
from activity_monitor import ActivityMonitor, StatusOptions, Timer


@pytest.fixture
def activity_monitor():
    return ActivityMonitor()


def test_timer_stops_correctly(activity_monitor):
    assert activity_monitor.active_users == 0
    assert activity_monitor.timer.is_running
    assert activity_monitor.status == StatusOptions.RUNNING

    activity_monitor.active_users = 1

    assert activity_monitor.active_users == 1
    assert not activity_monitor.timer.is_running
    assert activity_monitor.status == StatusOptions.RUNNING


def test_timer_starts_correctly(activity_monitor):
    activity_monitor.active_users = 2

    assert activity_monitor.active_users == 2
    assert not activity_monitor.timer.is_running
    assert activity_monitor.status == StatusOptions.RUNNING

    activity_monitor.active_users = 0

    assert activity_monitor.active_users == 0
    assert activity_monitor.timer.is_running
    assert activity_monitor.status == StatusOptions.RUNNING


@pytest.mark.asyncio
async def test_callback_updates_status(activity_monitor):
    assert activity_monitor.status == StatusOptions.RUNNING

    await activity_monitor.callback()

    assert activity_monitor.status == StatusOptions.STOPPED


@pytest.mark.asyncio
async def test_status_updates_to_stopped_when_timer_expires(activity_monitor):
    assert activity_monitor.active_users == 0
    assert activity_monitor.timer.is_running
    assert activity_monitor.status == StatusOptions.RUNNING

    activity_monitor.timer = Timer(timeout=1, callback=activity_monitor.callback)
    await asyncio.sleep(1.2)

    assert activity_monitor.status == StatusOptions.STOPPED
