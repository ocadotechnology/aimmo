import asyncio
import time
from unittest import mock

import pytest
from activity_monitor import ActivityMonitor, Timer


@pytest.fixture
def activity_monitor():
    return ActivityMonitor(mock.MagicMock())


def test_timer_stops_correctly(activity_monitor):
    assert activity_monitor.active_users == 0
    assert activity_monitor.timer.is_running

    activity_monitor.active_users = 1

    assert activity_monitor.active_users == 1
    assert not activity_monitor.timer.is_running


def test_timer_starts_correctly(activity_monitor):
    activity_monitor.active_users = 2

    assert activity_monitor.active_users == 2
    assert not activity_monitor.timer.is_running

    activity_monitor.active_users = 0

    assert activity_monitor.active_users == 0
    assert activity_monitor.timer.is_running


@pytest.mark.asyncio
async def test_callback_called_when_timer_expires(activity_monitor):
    assert activity_monitor.active_users == 0
    assert activity_monitor.timer.is_running

    activity_monitor.timer = Timer(timeout=1, callback=activity_monitor.callback)
    await asyncio.sleep(1.2)

    activity_monitor.callback.assert_called()
