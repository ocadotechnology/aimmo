import logging
from abc import ABCMeta, abstractmethod
from threading import Thread

from simulation.action import PRIORITIES

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

    @abstractmethod
    def run_turn(self, player_id_to_serialised_actions):
        pass

    def _run_turn_for_avatar(self, avatar, serialised_action):
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

    def _update_environment(self, game_state):
        num_avatars = len(game_state.avatar_manager.active_avatars)
        game_state.world_map.reconstruct_interactive_state(num_avatars)

    def _mark_complete(self):
        self.communicator.mark_game_complete(data=self.game_state.serialise())

    def run_single_turn(self, player_id_to_serialised_actions):
        self.run_turn(player_id_to_serialised_actions)
        self.game_state.update_environment()


class SequentialSimulationRunner(SimulationRunner):
    def run_turn(self, player_id_to_serialised_actions):
        """
        Get and apply each avatar's action in turn.
        """
        avatars = self.game_state.avatar_manager.active_avatars

        for avatar in avatars:
            self._run_turn_for_avatar(avatar, player_id_to_serialised_actions[avatar.player_id])
            location_to_clear = avatar.action.target_location
            avatar.action.process(self.game_state.world_map)
            self.game_state.world_map.clear_cell_actions(location_to_clear)


class ConcurrentSimulationRunner(SimulationRunner):
    def run_turn(self, player_id_to_serialised_actions):
        """
        Concurrently get the intended actions from all avatars and register
        them on the world map. Then apply actions in order of priority.
        """

        avatars = self.game_state.avatar_manager.active_avatars

        threads = [Thread(target=self._run_turn_for_avatar,
                          args=(avatar, player_id_to_serialised_actions[avatar.player_id])) for avatar in avatars]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        # Waits applied first, then attacks, then moves.
        avatars.sort(key=lambda a: PRIORITIES[type(a.action)])

        locations_to_clear = {a.action.target_location for a in avatars
                              if a.action is not None}

        for action in (a.action for a in avatars if a.action is not None):
            action.process(self.game_state.world_map)

        for location in locations_to_clear:
            self.game_state.world_map.clear_cell_actions(location)
