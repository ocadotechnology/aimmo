import os
import random
import string

import mock
import pytest
import socketio

TIME_TO_PROCESS_SOME_EVENT_LOOP = 0.1


async def test_send_updates_for_one_user(game_api, client, socketio_server, loop):
    socketio_client = socketio.AsyncClient(reconnection=False)
    mock_listener = mock.MagicMock()

    game_api.game_state.avatar_manager.add_avatar(1)

    socketio_client.on("game-state", mock_listener)

    avatar = game_api.game_state.avatar_manager.get_avatar(1)
    avatar.logs = ["Avatar log"]

    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    await game_api.send_updates_to_all()

    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    await socketio_client.disconnect()

    expected_game_state = game_api.game_state.serialize()
    expected_game_state["playerLog"] = "Avatar log"
    mock_listener.assert_has_calls([mock.call(expected_game_state)])


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
