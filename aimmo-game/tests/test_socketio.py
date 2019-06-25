import asyncio
import os
import random
import string
from unittest import TestCase, mock

import pytest
import service
from asynctest import CoroutineMock
from simulation.game_runner import GameRunner

from .test_simulation.mock_worker_manager import MockWorkerManager


class MockGameState(object):
    turn_count = 0

    def serialize(self):
        return {"foo": "bar"}


class MockedSocketIOServer(mock.MagicMock):
    """ Decorator function that just returns the function. Needed because we decorate
        functions in the GameAPI."""

    def on(self, event):
        def decorator(func):
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)

            return wrapper

        return decorator


class TestSocketIO:
    def setup_method(self, method):
        os.environ["GAME_ID"] = "1"
        self.environ = {"QUERY_STRING": "avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"}
        self.game_api = self.create_game_api()
        self.mocked_mappings = self.game_api._socket_session_id_to_player_id
        self.sid = "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(19)
        )

    def teardown_method(self, method):
        del os.environ["GAME_ID"]

    @mock.patch("docker.from_env")
    @mock.patch("service.app")
    def create_game_api(self, app, docker_from_env):
        game_runner = GameRunner(
            game_state_generator=lambda avatar_manager: MockGameState(),
            django_api_url="http://test",
            port="0000",
            worker_manager_class=MockWorkerManager,
        )
        return service.GameAPI(
            game_state=game_runner.game_state, worker_manager=game_runner.worker_manager
        )

    @pytest.mark.asyncio
    @mock.patch("service.app")
    @mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
    async def test_socketio_emit_called(self, mocked_socketio, app):
        self.game_api.worker_manager.add_new_worker(1)

        await self.game_api.register_world_update_on_connect()(self.sid, self.environ)

        assert mocked_socketio.manager.emit.mockreturn_value.emit.assert_called_once

    @pytest.mark.asyncio
    @mock.patch("service.app")
    @mock.patch("service.socketio_server.emit", new_callable=CoroutineMock())
    @mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
    async def test_matched_session_id_to_avatar_id_mapping(
        self, mocked_socketio, mocked_emit, app
    ):
        assert len(self.mocked_mappings) == 0

        self.game_api.worker_manager.add_new_worker(1)
        await self.game_api.register_world_update_on_connect()(self.sid, self.environ),

        assert len(self.mocked_mappings) == 1
        assert self.sid in self.mocked_mappings
        assert int(self.mocked_mappings[self.sid]) == 1

    @pytest.mark.asyncio
    @mock.patch("service.app")
    @mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
    async def test_no_match_session_id_to_avatar_id_mapping(self, mocked_socketio, app):
        self.environ["QUERY_STRING"] = "corrupted!@$%string123"

        assert len(self.mocked_mappings) == 0

        self.game_api.worker_manager.add_new_worker(1)

        await self.game_api.register_world_update_on_connect()(self.sid, self.environ),

        assert len(self.mocked_mappings) == 0
        assert not self.sid in self.mocked_mappings

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

        with mock.patch(
            "service.socketio_server.emit", new=CoroutineMock()
        ) as mocked_emit:
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

        with mock.patch(
            "service.socketio_server.emit", new=CoroutineMock()
        ) as mocked_emit:
            await self.game_api.send_updates()

            mocked_emit.assert_called_once_with(
                "game-state", {"foo": "bar"}, room=self.sid
            )

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

        with mock.patch(
            "service.socketio_server.emit", new=CoroutineMock()
        ) as mocked_emit:
            await self.game_api.send_updates()

            mocked_emit.assert_called_once_with(
                "game-state", {"foo": "bar"}, room=self.sid
            )

    @pytest.mark.asyncio
    @mock.patch("service.app")
    @mock.patch("service.socketio_server", new_callable=MockedSocketIOServer)
    async def test_send_updates_for_multiple_users(self, mocked_socketio, app):
        self.mocked_mappings[self.sid] = 1
        self.mocked_mappings["differentsid"] = 2

        self.game_api.worker_manager.add_new_worker(self.mocked_mappings[self.sid])
        self.game_api.worker_manager.add_new_worker(
            self.mocked_mappings["differentsid"]
        )
        worker_one = self.game_api.worker_manager.player_id_to_worker[
            self.mocked_mappings[self.sid]
        ]
        worker_two = self.game_api.worker_manager.player_id_to_worker[
            self.mocked_mappings["differentsid"]
        ]
        worker_one.log = "Logs one"
        worker_two.log = "Logs two"

        with mock.patch(
            "service.socketio_server.emit", new=CoroutineMock()
        ) as mocked_emit:
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

        with mock.patch(
            "service.socketio_server.emit", new=CoroutineMock()
        ) as mocked_emit:
            await self.game_api.send_updates()

            user_game_state_call = mock.call(
                "game-state", {"foo": "bar"}, room=self.sid
            )
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

        with mock.patch(
            "service.socketio_server.emit", new=CoroutineMock()
        ) as mocked_emit:
            await self.game_api.send_updates()

            mocked_emit.assert_called_once_with(
                "game-state", {"foo": "bar"}, room=self.sid
            )

    @pytest.mark.asyncio
    async def test_remove_session_id_on_disconnect(self):
        self.mocked_mappings[self.sid] = 1
        assert len(self.mocked_mappings) == 1
        assert self.sid in self.mocked_mappings
        assert self.mocked_mappings[self.sid] == 1

        await self.game_api.register_remove_session_id_from_mappings()(sid=self.sid)

        assert self.sid not in self.mocked_mappings
        assert len(self.mocked_mappings) == 0
