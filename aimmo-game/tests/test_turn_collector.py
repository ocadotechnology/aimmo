from typing import TYPE_CHECKING

import pytest
from aiohttp import web
from socketio import AsyncClient

from service import setup_socketIO_server
from turn_collector import TurnCollector
from .test_socketio import TIME_TO_PROCESS_SOME_EVENT_LOOP

if TYPE_CHECKING:
    from turn_collector import CollectedTurnActions


def test_calling_new_turn_gives_new_collected_turn_actions(turn_collector):
    turn_collector.new_turn(1)
    turn_1: "CollectedTurnActions" = turn_collector.collected_turns
    turn_collector.new_turn(2)
    turn_2: "CollectedTurnActions" = turn_collector.collected_turns

    assert turn_1.turn_number == 1
    assert turn_2.turn_number == 2
    assert turn_1 != turn_2


async def test_new_actions_update_collected_turns(
    game_api, turn_collector, socketio_server, client, loop
):
    turn_collector.new_turn(1)

    socketio_client = AsyncClient(reconnection=False)
    await socketio_client.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=1&EIO=3&transport=polling&t=MJhoMgb"
    )

    wait_action = {"action_type": "wait"}
    await socketio_client.emit("action", wait_action)
    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    assert turn_collector.collected_turns.player_id_to_actions[1] == wait_action

    socketio_client_2 = AsyncClient(reconnection=False)
    await socketio_client_2.connect(
        f"http://{client.server.host}:{client.server.port}?avatar_id=2&EIO=3&transport=polling&t=MJhoMgb"
    )

    move_action = {"action_type": "move", "options": {"x": 1, "y": 2}}
    await socketio_client_2.emit("action", move_action)
    await socketio_server.sleep(TIME_TO_PROCESS_SOME_EVENT_LOOP)
    assert turn_collector.collected_turns.player_id_to_actions[2] == move_action
    assert len(turn_collector.collected_turns.player_id_to_actions) == 2

    await socketio_client.disconnect()
    await socketio_client_2.disconnect()
