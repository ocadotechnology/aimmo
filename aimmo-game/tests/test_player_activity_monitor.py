import asyncio

import pytest
from player_activity_monitor import ActivityMonitor


@pytest.fixture
def activity_monitor():
    return ActivityMonitor()


def test_timer_stops_when_user_connects(activity_monitor):
    assert activity_monitor.active_users == 0
    assert activity_monitor.timer_running
    assert activity_monitor._status == activity_monitor.status_options.RUNNING

    activity_monitor.update_active_users(1)
    activity_monitor.check_active_users()

    assert activity_monitor.active_users == 1
    assert not activity_monitor.timer_running
    assert activity_monitor._status == activity_monitor.status_options.RUNNING


def test_timer_starts_when_users_disconnect(activity_monitor):
    activity_monitor.update_active_users(2)
    activity_monitor.check_active_users()

    assert activity_monitor.active_users == 2
    assert not activity_monitor.timer_running
    assert activity_monitor._status == activity_monitor.status_options.RUNNING

    activity_monitor.update_active_users(0)
    activity_monitor.check_active_users()

    assert activity_monitor.active_users == 0
    assert activity_monitor.timer_running
    assert activity_monitor._status == activity_monitor.status_options.RUNNING


@pytest.mark.asyncio
async def test_status_updates_to_stopped_when_timer_expires(activity_monitor):
    assert activity_monitor.active_users == 0
    assert activity_monitor.timer_running
    assert activity_monitor._status == activity_monitor.status_options.RUNNING

    activity_monitor.timer = asyncio.ensure_future(asyncio.sleep(1))

    await activity_monitor.timer_completed()

    assert activity_monitor._status == activity_monitor.status_options.STOPPED
