import asyncio
import logging
from typing import TYPE_CHECKING

from metrics import GAME_TURN_TIME
from simulation.avatar.avatar_manager import AvatarManager
from simulation.django_communicator import (
    DjangoCommunicator,
    GameMetadataFetchFailedError,
)
from simulation.simulation_runner import ConcurrentSimulationRunner

if TYPE_CHECKING:
    from turn_collector import TurnCollector
    from simulation.game_state import GameState

LOGGER = logging.getLogger(__name__)

TURN_TIME = 2


class GameRunner:
    def __init__(
        self,
        game_state_generator,
        communicator: DjangoCommunicator,
        port,
        turn_collector: "TurnCollector",
    ):
        super(GameRunner, self).__init__()

        self.game_state: "GameState" = game_state_generator(AvatarManager())
        self.communicator = communicator
        self.simulation_runner = ConcurrentSimulationRunner(
            communicator=self.communicator, game_state=self.game_state
        )
        self.turn_collector = turn_collector
        self.turn_collector.new_turn(self.game_state.turn_count)
        self._end_turn_callback = lambda: None

    def set_end_turn_callback(self, callback_method):
        self._end_turn_callback = callback_method

    def get_users_to_add(self, game_metadata):
        def player_is_new(_player):
            return (
                _player["id"]
                not in self.simulation_runner.game_state.avatar_manager.avatars_by_id.keys()
            )

        return [
            player["id"] for player in game_metadata["users"] if player_is_new(player)
        ]

    def get_users_to_delete(self, game_metadata):
        def player_in_avatar_manager_but_not_metadata(pid):
            return pid not in [player["id"] for player in game_metadata["users"]]

        return [
            player_id
            for player_id in self.simulation_runner.game_state.avatar_manager.avatars_by_id.keys()
            if player_in_avatar_manager_but_not_metadata(player_id)
        ]

    async def update_avatars(self):
        try:
            game_metadata = await self.communicator.get_game_metadata()
            users_to_add = self.get_users_to_add(game_metadata)
            users_to_delete = self.get_users_to_delete(game_metadata)

            self.simulation_runner.add_avatars(users_to_add)
            self.simulation_runner.delete_avatars(users_to_delete)
        except GameMetadataFetchFailedError:
            LOGGER.error("Game metadata fetch failed, not updating avatars this turn")
            pass

    async def update_simulation(self, player_id_to_serialized_actions):
        await self.simulation_runner.run_single_turn(player_id_to_serialized_actions)
        await self._end_turn_callback()
        self.game_state.turn_count += 1

    async def update(self):
        with GAME_TURN_TIME():
            await self.update_avatars()
            await self.update_simulation(self.turn_collector.collected_turns)
            self.game_state.avatar_manager.clear_all_avatar_logs()
            self.turn_collector.new_turn(self.game_state.turn_count)

    def _get_task_result_or_stop_loop(self, task):
        try:
            task.result()
        except Exception as e:
            LOGGER.exception(f"Unexpected error, stopping game loop: {e}")
            loop = asyncio.get_event_loop()
            loop.stop()

    async def run(self):
        while True:
            LOGGER.info(f"Starting turn {self.game_state.turn_count}")
            turn = asyncio.ensure_future(self.update())

            turn.add_done_callback(self._get_task_result_or_stop_loop)

            await asyncio.sleep(TURN_TIME)
            await turn
