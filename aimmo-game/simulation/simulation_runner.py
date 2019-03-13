import asyncio
import logging
import threading
from abc import ABCMeta, abstractmethod
from threading import Thread

from simulation.action import PRIORITIES, WaitAction

LOGGER = logging.getLogger(__name__)

TURN_INTERVAL = 2


class SimulationRunner(object):
    """
    Game loop
    """
    daemon = True
    __metaclass__ = ABCMeta

    def __init__(self, game_state, communicator):
        self.game_state = game_state
        self.communicator = communicator
        self._lock = threading.RLock()

    @abstractmethod
    async def run_turn(self, player_id_to_serialised_actions):
        pass

    async def _run_turn_for_avatar(self, avatar, serialised_action):
        """
        Send an avatar its view of the game state and register its
        chosen action & logs.
        """
        self._register_actions(avatar, serialised_action)

    def _register_actions(self, avatar, serialised_action):
        """
        Calls a function that constructs the action object, does error handling,
        and finally registers it onto the avatar.

        :param avatar: Avatar wrapper object
        :param serialised_action: A string representing the action
        """
        if avatar.decide_action(serialised_action):
            avatar.action.register(self.game_state.world_map)

    def _update_effects(self):
        with self._lock:
            for avatar in self.game_state.avatar_manager.active_avatars:
                avatar.update_effects()

    def update_environment(self):
        with self._lock:
            self._update_effects()
            num_avatars = len(self.game_state.avatar_manager.active_avatars)
            self.game_state.world_map.update(num_avatars)

    def _mark_complete(self):
        self.communicator.mark_game_complete(data=self.game_state.serialise())

    def add_avatar(self, player_id, location=None):
        with self._lock:
            location = self.game_state.world_map.get_random_spawn_location() if location is None else location
            avatar = self.game_state.avatar_manager.add_avatar(player_id, location)
            self.game_state.world_map.get_cell(location).avatar = avatar

    def remove_avatar(self, player_id):
        with self._lock:
            try:
                avatar = self.game_state.avatar_manager.get_avatar(player_id)
            except KeyError:
                return
            self.game_state.world_map.get_cell(avatar.location).avatar = None
            self.game_state.avatar_manager.remove_avatar(player_id)

    def add_avatars(self, player_ids):
        for player_id in player_ids:
            self.add_avatar(player_id)

    def delete_avatars(self, player_ids):
        for player_id in player_ids:
            self.remove_avatar(player_id)

    async def run_single_turn(self, player_id_to_serialised_actions):
        await self.run_turn(player_id_to_serialised_actions)
        self.update_environment()


class SequentialSimulationRunner(SimulationRunner):
    async def run_turn(self, player_id_to_serialised_actions):
        """
        Get and apply each avatar's action in turn.
        """
        avatars = self.game_state.avatar_manager.active_avatars

        for avatar in avatars:
            await self._run_turn_for_avatar(avatar, player_id_to_serialised_actions[avatar.player_id])
            location_to_clear = avatar.action.target_location
            avatar.action.process(self.game_state.world_map)
            self.game_state.world_map.clear_cell_actions(location_to_clear)


class ConcurrentSimulationRunner(SimulationRunner):
    async def async_map(self, func, iterable_args):
        futures = [func(*arg) for arg in iterable_args]
        await asyncio.gather(*futures)

    async def run_turn(self, player_id_to_serialised_actions):
        """
        Concurrently get the intended actions from all avatars and register
        them on the world map. Then apply actions in order of priority.
        """

        avatars = self.game_state.avatar_manager.active_avatars
        args = [(avatar, player_id_to_serialised_actions[avatar.player_id]) for avatar in avatars]
        await self.async_map(self._run_turn_for_avatar, args)

        # Waits applied first, then attacks, then moves.
        avatars.sort(key=lambda a: PRIORITIES[type(a.action)])

        locations_to_clear = {a.action.target_location for a in avatars
                              if a.action is not None}

        for action in (a.action for a in avatars if a.action is not None):
            action.process(self.game_state.world_map)

        for location in locations_to_clear:
            self.game_state.world_map.clear_cell_actions(location)
