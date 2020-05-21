import os
import random
import string

import mock
import pytest
import socketio

TIME_TO_PROCESS_SOME_EVENT_LOOP = 0.1


async def test_socketio_emit_called_when_worker_ready(
    game_api, socketio_server, client, loop
):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_game_state_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("game-state", mock_game_state_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker.ready = True

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_game_state_listener.assert_called_once()


async def test_socketio_emit_not_called_if_worker_not_ready(
    game_api, socketio_server, client, loop
):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_game_state_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("game-state", mock_game_state_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    assert worker.ready == False

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_game_state_listener.assert_not_called()


async def test_send_updates_for_one_user(game_api, client, socketio_server, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_log_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("log", mock_log_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker.logs = ["Logs one"]

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_log_listener.assert_has_calls(
        [mock.call({"message": "Logs one", "turn_count": 0})]
    )


async def test_send_worker_and_avatar_logs_for_one_user(
    game_api, client, socketio_server, loop
):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_log_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("log", mock_log_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker.logs = ["Worker log"]

    avatar = game_api.game_state.avatar_manager.get_avatar(1)
    avatar.logs = ["Avatar log"]

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_log_listener.assert_has_calls(
        [mock.call({"message": "Worker log\nAvatar log", "turn_count": 0})]
    )


async def test_no_logs_not_emitted(game_api, client, socketio_server, loop):
    """ If there are no logs for an avatar, no logs should be emitted. """
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_log_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("log", mock_log_listener)

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_log_listener.assert_not_called()


async def test_empty_logs_not_emitted(game_api, client, socketio_server, loop):
    """ If the logs are an empty sting, no logs should be emitted. """
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_log_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("log", mock_log_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker.logs = []

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_log_listener.assert_not_called()


async def test_send_updates_for_multiple_users(game_api, client, socketio_server, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)
    socketio_client2 = socketio.AsyncClient(reconnection=False)
    mock_log_listener = mock.MagicMock()
    mock_log_listener2 = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)
    game_api.worker_manager.add_new_worker(2)
    game_api.game_state.avatar_manager.add_avatar(2)

    socketio_client.on("log", mock_log_listener)
    socketio_client2.on("log", mock_log_listener2)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker2 = game_api.worker_manager.player_id_to_worker[2]
    worker.logs = ["Logs one"]
    worker2.logs = ["Logs two"]

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await socketio_client2.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=2&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()
    await socketio_client2.disconnect()

    mock_log_listener.assert_has_calls(
        [mock.call({"message": "Logs one", "turn_count": 0})]
    )
    mock_log_listener2.assert_has_calls(
        [mock.call({"message": "Logs two", "turn_count": 0})]
    )


async def test_send_code_changed_flag(game_api, client, socketio_server, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_avatar_updated_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("feedback-avatar-updated", mock_avatar_updated_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker.has_code_updated = True

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_avatar_updated_listener.assert_called_once()


async def test_send_false_flag_not_sent(game_api, client, socketio_server, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_avatar_updated_listener = mock.MagicMock()

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("feedback-avatar-updated", mock_avatar_updated_listener)

    worker = game_api.worker_manager.player_id_to_worker[1]
    worker.has_code_updated = False

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    mock_avatar_updated_listener.assert_not_called()


async def test_remove_session_id_on_disconnect(game_api, client, socketio_server, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)

    game_api.worker_manager.add_new_worker(1)
    game_api.game_state.avatar_manager.add_avatar(1)

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)

    assert len(socketio_server.eio.sockets) == 1

    await socketio_client.disconnect()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)

    assert len(socketio_server.eio.sockets) == 0
