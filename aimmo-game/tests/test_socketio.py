import asyncio
import os
import random
import string
import socketio
import logging
from unittest import TestCase, mock
from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from prometheus_client import make_wsgi_app

import pytest
import time

import service
from asynctest import CoroutineMock
from simulation.game_runner import GameRunner

from .test_simulation.mock_communicator import MockCommunicator
from .test_simulation.mock_worker_manager import MockWorkerManager


class MockGameState(object):
    turn_count = 0

    def serialize(self):
        return {"foo": "bar"}


@pytest.fixture
def game_id():
    os.environ["GAME_ID"] = "1"
    yield
    del os.environ["GAME_ID"]


@pytest.fixture
def sid():
    return "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(19)
    )


@pytest.fixture
def app():
    return service.app_setup(should_clean_token=False)


@pytest.fixture
def socketio_server(app):
    return service.socketIO_setup(app, async_handlers=False)


@pytest.fixture
def game_api(app, socketio_server, game_id):
    game_runner = GameRunner(
        game_state_generator=lambda avatar_manager: MockGameState(),
        communicator=MockCommunicator(),
        port="0000",
        worker_manager_class=MockWorkerManager,
    )
    return service.GameAPI(
        game_state=game_runner.game_state,
        worker_manager=game_runner.worker_manager,
        web_app=app,
        socketio_server2=socketio_server,
    )


@pytest.fixture
def client(app, aiohttp_client, loop):
    return loop.run_until_complete(aiohttp_client(app))


async def test_socketio_emit_called(game_api, socketio_server, client, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_game_state_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)

    socketio_client.on("game-state", mock_game_state_listener)

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await socketio_server.sleep(0.0001)

    mock_game_state_listener.assert_called_once()


@pytest.mark.asyncio
@mock.patch("service.app")
@mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
async def test_send_updates_for_one_user(self, mocked_socketio, app):
    self.mocked_mappings[self.sid] = 1
    self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
    worker = self.game_api.worker_manager.player_id_to_worker[
        self.mocked_mappings[self.sid]
    ]
    worker.log = "Logs one"

    with mock.patch("service.socketio_server.emit", new=CoroutineMock()) as mocked_emit:
        await self.game_api.send_updates()

        game_state_call = mock.call("game-state", {"foo": "bar"}, room=self.sid)
        log_call = mock.call(
            "log", {"message": "Logs one", "turn_count": 0}, room=self.sid
        )

        mocked_emit.assert_has_calls([game_state_call, log_call], any_order=True)


@pytest.mark.asyncio
@mock.patch("service.app")
@mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
async def test_no_logs_not_emitted(self, mocked_socketio, app):
    """ If there are no logs for an avatar, no logs should be emitted. """
    self.mocked_mappings[self.sid] = 1
    self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])

    with mock.patch("service.socketio_server.emit", new=CoroutineMock()) as mocked_emit:
        await self.game_api.send_updates()

        mocked_emit.assert_called_once_with("game-state", {"foo": "bar"}, room=self.sid)


@pytest.mark.asyncio
@mock.patch("service.app")
@mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
async def test_empty_logs_not_emitted(self, mocked_socketio, app):
    """ If the logs are an empty sting, no logs should be emitted. """
    self.mocked_mappings[self.sid] = 1

    self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
    worker = self.game_api.worker_manager.player_id_to_worker[
        self.mocked_mappings[self.sid]
    ]
    worker.logs = ""

    with mock.patch("service.socketio_server.emit", new=CoroutineMock()) as mocked_emit:
        await self.game_api.send_updates()

        mocked_emit.assert_called_once_with("game-state", {"foo": "bar"}, room=self.sid)


@pytest.mark.asyncio
@mock.patch("service.app")
@mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
async def test_send_updates_for_multiple_users(self, mocked_socketio, app):
    self.mocked_mappings[self.sid] = 1
    self.mocked_mappings["differentsid"] = 2

    self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
    self.game_api.worker_manager.add_new_worker(self.mocked_mappings["differentsid"])
    worker_one = self.game_api.worker_manager.player_id_to_worker[
        self.mocked_mappings[self.sid]
    ]
    worker_two = self.game_api.worker_manager.player_id_to_worker[
        self.mocked_mappings["differentsid"]
    ]
    worker_one.log = "Logs one"
    worker_two.log = "Logs two"

    with mock.patch("service.socketio_server.emit", new=CoroutineMock()) as mocked_emit:
        await self.game_api.send_updates()

        user_one_game_state_call = mock.call(
            "game-state", {"foo": "bar"}, room=self.sid
        )
        user_two_game_state_call = mock.call(
            "game-state", {"foo": "bar"}, room="differentsid"
        )
        user_one_log_call = mock.call(
            "log", {"message": "Logs one", "turn_count": 0}, room=self.sid
        )
        user_two_log_call = mock.call(
            "log", {"message": "Logs two", "turn_count": 0}, room="differentsid"
        )

        mocked_emit.assert_has_calls(
            [
                user_one_game_state_call,
                user_two_game_state_call,
                user_one_log_call,
                user_two_log_call,
            ],
            any_order=True,
        )


@pytest.mark.asyncio
@mock.patch("service.app")
@mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
async def test_send_code_changed_flag(self, mocked_socketio, app):
    self.mocked_mappings[self.sid] = 1
    self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
    worker = self.game_api.worker_manager.player_id_to_worker[
        self.mocked_mappings[self.sid]
    ]
    worker.has_code_updated = True

    with mock.patch("service.socketio_server.emit", new=CoroutineMock()) as mocked_emit:
        await self.game_api.send_updates()

        user_game_state_call = mock.call("game-state", {"foo": "bar"}, room=self.sid)
        user_game_code_changed_call = mock.call(
            "feedback-avatar-updated", {}, room=self.sid
        )

        mocked_emit.assert_has_calls(
            [user_game_state_call, user_game_code_changed_call], any_order=True
        )


@pytest.mark.asyncio
@mock.patch("service.app")
@mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
async def test_send_false_flag_not_sent(self, mocked_socketio, app):
    self.mocked_mappings[self.sid] = 1
    self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
    worker = self.game_api.worker_manager.player_id_to_worker[
        self.mocked_mappings[self.sid]
    ]
    worker.has_code_updated = False

    with mock.patch("service.socketio_server.emit", new=CoroutineMock()) as mocked_emit:
        await self.game_api.send_updates()

        mocked_emit.assert_called_once_with("game-state", {"foo": "bar"}, room=self.sid)


@pytest.mark.asyncio
async def test_remove_session_id_on_disconnect(self):
    self.mocked_mappings[self.sid] = 1
    assert len(self.mocked_mappings) == 1
    assert self.sid in self.mocked_mappings
    assert self.mocked_mappings[self.sid] == 1

    await self.game_api.register_remove_session_id_from_mappings()(sid=self.sid)

    assert self.sid not in self.mocked_mappings
    assert len(self.mocked_mappings) == 0
