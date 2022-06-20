import asyncio
import threading
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from simulation.action import PRIORITIES
from simulation.game_logic import EffectApplier, MapContext
from simulation.worksheet.worksheet import WorksheetData, get_worksheet_data

if TYPE_CHECKING:
    from turn_collector import CollectedTurnActions

TURN_INTERVAL = 2


class SimulationRunner(object):
    """
    Game loop
    """

    daemon = True
    __metaclass__ = ABCMeta

    def __init__(self, game_state, communicator, worksheet: WorksheetData = None):
        if worksheet is None:
            worksheet = get_worksheet_data()

        self.game_state = game_state
        self.communicator = communicator
        self.worksheet: WorksheetData = worksheet
        self._lock = threading.RLock()

    @abstractmethod
    async def run_turn(self, collected_turn_actions: "CollectedTurnActions"):
        pass

    async def _run_turn_for_avatar(self, avatar, serialized_action):
        """
        Send an avatar its view of the game state and register its
        chosen action & logs.
        """
        self._register_actions(avatar, serialized_action)

    def _register_actions(self, avatar, serialized_action):
        """
        Calls a function that constructs the action object, does error handling,
        and finally registers it onto the avatar.

        :param avatar: Avatar wrapper object
        :param serialized_action: A string representing the action
        """
        if avatar.decide_action(serialized_action):
            avatar.action.register(self.game_state.world_map)

    def _update_effects(self):
        with self._lock:
            for avatar in self.game_state.avatar_manager.active_avatars:
                avatar.update_effects()

    def update_environment(self):
        with self._lock:
            self._update_effects()
            num_avatars = len(self.game_state.avatar_manager.active_avatars)
            self.update(num_avatars, self.game_state)

    def update(self, num_avatars, game_state):
        EffectApplier().apply(game_state)
        self._update_map(num_avatars)

    def _update_map(self, num_avatars):
        context = MapContext(num_avatars=num_avatars)
        for map_updater in self.worksheet.map_updaters:
            map_updater.update(self.game_state.world_map, context=context)

    def add_avatar(self, player_id, location=None):
        with self._lock:
            location = (
                self.game_state.world_map.get_random_spawn_location()
                if location is None
                else location
            )
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

    async def run_single_turn(self, collected_turn_actions: "CollectedTurnActions"):
        await self.run_turn(collected_turn_actions)
        self.update_environment()


class SequentialSimulationRunner(SimulationRunner):
    async def run_turn(self, collected_turn_actions: "CollectedTurnActions"):
        """
        Get and apply each avatar's action in turn.
        """
        avatars = self.game_state.avatar_manager.active_avatars

        for avatar in avatars:
            await self._run_turn_for_avatar(
                avatar, collected_turn_actions.get_action_for_player(avatar.player_id)
            )
            location_to_clear = avatar.action.target_location
            avatar.action.process(self.game_state.world_map)
            self.game_state.world_map.clear_cell_actions(location_to_clear)


class ConcurrentSimulationRunner(SimulationRunner):
    async def async_map(self, func, iterable_args):
        futures = [func(*arg) for arg in iterable_args]
        await asyncio.gather(*futures)

    async def run_turn(self, collected_turn_actions: "CollectedTurnActions"):
        """
        Concurrently get the intended actions from all avatars and register
        them on the world map. Then apply actions in order of priority.
        """

        avatars = self.game_state.avatar_manager.active_avatars
        args = [
            (avatar, collected_turn_actions.get_action_for_player(avatar.player_id))
            for avatar in avatars
        ]
        await self.async_map(self._run_turn_for_avatar, args)

        # Waits applied first, then attacks, then moves.
        avatars.sort(key=lambda a: PRIORITIES[type(a.action)])

        locations_to_clear = {
            a.action.target_location for a in avatars if a.action is not None
        }

        for action in (a.action for a in avatars if a.action is not None):
            action.process(self.game_state.world_map)

        for location in locations_to_clear:
            self.game_state.world_map.clear_cell_actions(location)
