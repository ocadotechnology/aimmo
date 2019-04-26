import asyncio
import concurrent.futures
import logging
import threading
import time

from prometheus_client import Histogram

from metrics import GAME_TURN_TIME
from simulation.avatar.avatar_manager import AvatarManager
from simulation.django_communicator import DjangoCommunicator
from simulation.simulation_runner import ConcurrentSimulationRunner
from simulation.worker_manager import WorkerManager

LOGGER = logging.getLogger(__name__)

TURN_TIME = 2


class GameRunner:
    def __init__(
        self,
        game_state_generator,
        django_api_url,
        port,
        worker_manager_class=WorkerManager,
    ):
        super(GameRunner, self).__init__()

        self.worker_manager = worker_manager_class(port=port)
        self.game_state = game_state_generator(AvatarManager())
        self.communicator = DjangoCommunicator(
            django_api_url=django_api_url, completion_url=django_api_url + "complete/"
        )
        self.simulation_runner = ConcurrentSimulationRunner(
            communicator=self.communicator, game_state=self.game_state
        )
        self._end_turn_callback = lambda: None

    def set_end_turn_callback(self, callback_method):
        self._end_turn_callback = callback_method

    def get_users_to_add(self, game_metadata):
        def player_is_new(_player):
            return _player["id"] not in self.worker_manager.player_id_to_worker.keys()

        return [
            player["id"] for player in game_metadata["users"] if player_is_new(player)
        ]

    def get_users_to_delete(self, game_metadata):
        def player_in_worker_manager_but_not_metadata(pid):
            return pid not in [player["id"] for player in game_metadata["users"]]

        return [
            player_id
            for player_id in self.worker_manager.player_id_to_worker.keys()
            if player_in_worker_manager_but_not_metadata(player_id)
        ]

    def update_main_user(self, game_metadata):
        self.game_state.main_avatar_id = game_metadata["main_avatar"]

    async def update_workers(self):
        game_metadata = self.communicator.get_game_metadata()["main"]

        users_to_add = self.get_users_to_add(game_metadata)
        users_to_delete = self.get_users_to_delete(game_metadata)

        await self.worker_manager.add_workers(users_to_add)
        await self.worker_manager.delete_workers(users_to_delete)
        self.simulation_runner.add_avatars(users_to_add)
        self.simulation_runner.delete_avatars(users_to_delete)
        await self.worker_manager.update_worker_codes(game_metadata["users"])

        self.update_main_user(game_metadata)
        self.worker_manager.fetch_all_worker_data(
            self.game_state.get_serialized_game_states_for_workers()
        )

    async def update_simulation(self, player_id_to_serialized_actions):
        await self.simulation_runner.run_single_turn(player_id_to_serialized_actions)
        await self._end_turn_callback()

    async def update(self):
        with GAME_TURN_TIME():
            await self.update_workers()
            await self.update_simulation(
                self.worker_manager.get_player_id_to_serialized_actions()
            )
            self.worker_manager.clear_logs()
            self.game_state.turn_count += 1

    async def run(self):
        while True:
            await self.update()
