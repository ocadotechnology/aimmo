from logging import getLogger
from abc import ABCMeta, abstractmethod
from simulation.direction import Direction
from simulation.event import FailedAttackEvent, FailedMoveEvent, MovedEvent, PerformedAttackEvent, ReceivedAttackEvent

LOGGER = getLogger(__name__)

LOGGER = getLogger(__name__)


class Action(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _do_action(self, game_state, avatar):
        raise NotImplementedError()

    def apply(self, game_state, avatar):
        self._do_action(game_state, avatar)
        cell = game_state.world_map.get_cell(avatar.location)
        self._add_score_from_cell_if_needed(avatar, cell)
        if cell.pickup is not None:
            cell.pickup.apply(avatar)

    def _add_score_from_cell_if_needed(self, avatar, cell):
        if cell.generates_score:
            avatar.score += 1

    def __str__(self):
        return self.__class__.__name__


class WaitAction(Action):
    def _do_action(self, game_state, avatar):
        pass


class MoveAction(Action):
    def __init__(self, direction):
        # Untrusted data!
        self.direction = Direction(**direction)

    def _do_action(self, game_state, avatar):
        target_location = avatar.location + self.direction
        if game_state.world_map.can_move_to(target_location):
            avatar.add_event(MovedEvent(avatar.location, target_location))
            game_state.world_map.get_cell(avatar.location).avatar = None
            avatar.location = target_location
            new_cell = game_state.world_map.get_cell(target_location)
            new_cell.avatar = avatar
        else:
            avatar.add_event(FailedMoveEvent(avatar.location, target_location))


class AttackAction(Action):
    def __init__(self, direction):
        # Untrusted data!
        self.direction = Direction(**direction)

    def _do_action(self, game_state, avatar):
        target_location = avatar.location + self.direction
        attacked_avatar = game_state.world_map.get_cell(target_location).avatar
        if attacked_avatar:
            damage_dealt = attacked_avatar.damage(avatar.attack_strength)
            avatar.add_event(PerformedAttackEvent(attacked_avatar, target_location, damage_dealt))
            attacked_avatar.add_event(ReceivedAttackEvent(avatar, damage_dealt))
            LOGGER.debug('{} dealt {} damage to {}'.format(avatar, damage_dealt, attacked_avatar))
            # TODO: refactor into AvatarWrapper.damage method
            if attacked_avatar.health <= 0:
                respawn_location = game_state.world_map.get_random_spawn_location()
                attacked_avatar.die(respawn_location)
                game_state.world_map.get_cell(target_location).avatar = None
                game_state.world_map.get_cell(respawn_location).avatar = attacked_avatar
        else:
            avatar.add_event(FailedAttackEvent(target_location))


ACTIONS = {
    'attack': AttackAction,
    'move': MoveAction,
    'wait': WaitAction,
}
