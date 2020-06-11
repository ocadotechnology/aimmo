import logging
from typing import TYPE_CHECKING, Dict
from dataclasses import dataclass, field

LOGGER = logging.getLogger(__name__)

if TYPE_CHECKING:
    from socketio import AsyncServer


@dataclass
class CollectedTurnActions:
    turn_number: int
    player_id_to_actions: Dict[int, object] = field(default_factory=dict)

    def get_action_for_player(self, player_id: int) -> object:
        try:
            return self.player_id_to_actions[player_id]
        except KeyError:
            return {"action_type": "wait"}


class TurnCollector:
    def __init__(self, socketio_server: "AsyncServer"):
        self.socketio_server = socketio_server
        self.register_action_received_event()

    def new_turn(self, turn_number):
        self.collected_turns = CollectedTurnActions(turn_number)

    def register_action_received_event(self):
        @self.socketio_server.on("action")
        async def action_received(sid, data):
            session_data = await self.socketio_server.get_session(sid)
            if data["turnCount"] == self.collected_turns.turn_number:
                player_id = session_data["id"]
                self.collected_turns.player_id_to_actions[player_id] = data["action"]

        return action_received
