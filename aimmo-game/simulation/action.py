from logging import getLogger
from simulation.direction import Direction
from simulation.event import FailedAttackEvent, FailedMoveEvent, MovedEvent, PerformedAttackEvent, ReceivedAttackEvent
import simulation.world_map as world_map_module

LOGGER = getLogger(__name__)


class Action(object):
    def __init__(self):
        self._avatar = None

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        self._avatar = value

    def apply(self, game_state):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def apply(self, game_state):
        _add_score_from_cell_if_needed(self.avatar, game_state)


class MoveAction(Action):
    def __init__(self, direction):
        super(MoveAction, self).__init__()
        # Untrusted data!
        self.direction = Direction(**direction)

    def apply(self, game_state):
        target_location = self.avatar.location + self.direction
        if game_state.world_map.can_move_to(target_location):
            self.avatar.add_event(MovedEvent(self.avatar.location, target_location))
            game_state.world_map.get_cell(self.avatar.location).avatar = None
            self.avatar.location = target_location
            new_cell = game_state.world_map.get_cell(target_location)
            new_cell.avatar = self.avatar
            if new_cell.pickup:
                # TODO: potentially extract pickup logic into pickup when adding multiple types
                self.avatar.health = min(10, self.avatar.health + new_cell.pickup.health_restored)
                new_cell.pickup = None
        else:
            self.avatar.add_event(FailedMoveEvent(self.avatar.location, target_location))
        _add_score_from_cell_if_needed(self.avatar, game_state)


class AttackAction(Action):
    def __init__(self, direction):
        super(AttackAction, self).__init__()
        # Untrusted data!
        self.direction = Direction(**direction)

    def apply(self, game_state):
        target_location = self.avatar.location + self.direction
        attacked_avatar = game_state.world_map.get_cell(target_location).avatar
        if attacked_avatar:
            damage_dealt = 1
            self.avatar.add_event(PerformedAttackEvent(attacked_avatar, target_location, damage_dealt))
            attacked_avatar.add_event(ReceivedAttackEvent(self.avatar, damage_dealt))
            attacked_avatar.health -= damage_dealt
            LOGGER.debug('{} dealt {} damage to {}'.format(self.avatar, damage_dealt, attacked_avatar))
            if attacked_avatar.health <= 0:
                respawn_location = game_state.world_map.get_random_spawn_location()
                attacked_avatar.die(respawn_location)
                game_state.world_map.get_cell(target_location).avatar = None
                game_state.world_map.get_cell(respawn_location).avatar = attacked_avatar
        else:
            self.avatar.add_event(FailedAttackEvent(target_location))
        _add_score_from_cell_if_needed(self.avatar, game_state)


# TODO: investigate moving this to after an action is handled - it is not specific to an action
def _add_score_from_cell_if_needed(avatar, game_state):
    cell = game_state.world_map.get_cell(avatar.location)
    if cell.generates_score:
        avatar.score += 1

ACTIONS = {
    'attack': AttackAction,
    'move': MoveAction,
    'wait': WaitAction,
}
