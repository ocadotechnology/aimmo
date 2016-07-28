from logging import getLogger
from simulation.direction import Direction
from simulation.event import FailedAttackEvent, FailedMoveEvent, MovedEvent, PerformedAttackEvent, ReceivedAttackEvent
import simulation.world_map as world_map_module

LOGGER = getLogger(__name__)


class Action(object):
    def __init__(self, avatar, priority):
        self._avatar = avatar
        self._priority = priority
        try:
            self._target_location = self._avatar.location + self.direction
        except AttributeError:
            self._target_location = self._avatar.location

    @property
    def avatar(self):
        return self._avatar

    @property
    def target_location(self):
        return self._target_location

    # Wait actions are applied first, then attack actions, then move actions.
    @property
    def priority(self):
        return self._priority

    def target(self, world_map):
        if world_map.is_on_map(self._target_location):
            world_map.get_cell(self._target_location).actions.append(self)

    def apply(self, world_map):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def __init__(self, avatar):
        super(WaitAction, self).__init__(avatar, priority=0)

    def apply(self, world_map):
        _add_score_from_cell_if_needed(self._avatar, world_map)


class MoveAction(Action):
    def __init__(self, avatar, direction):
        # Untrusted data!
        self.direction = Direction(**direction)
        super(MoveAction, self).__init__(avatar, priority=2)

    def apply(self, world_map):
        if world_map.can_move_to(self._target_location):

            event = MovedEvent(self._avatar.location, self._target_location)
            self._avatar.add_event(event)

            world_map.get_cell(self._avatar.location).avatar = None
            self._avatar.location = self._target_location

            new_cell = world_map.get_cell(self._target_location)
            new_cell.avatar = self._avatar

            if new_cell.pickup:
                # TODO: potentially extract pickup logic into pickup when adding multiple types
                self._avatar.health = min(10, self._avatar.health + new_cell.pickup.health_restored)
                new_cell.pickup = None
        else:
            self._avatar.add_event(FailedMoveEvent(self._avatar.location, self._target_location))
        _add_score_from_cell_if_needed(self._avatar, world_map)


class AttackAction(Action):
    def __init__(self, avatar, direction):
        # Untrusted data!
        self.direction = Direction(**direction)
        super(AttackAction, self).__init__(avatar, priority=1)

    def apply(self, world_map):
        attacked_avatar = world_map.attackable_avatar(self._target_location)
        if attacked_avatar:
            damage_dealt = 1
            self._avatar.add_event(PerformedAttackEvent(attacked_avatar, self._target_location, damage_dealt))
            attacked_avatar.add_event(ReceivedAttackEvent(self._avatar, damage_dealt))
            attacked_avatar.health -= damage_dealt
            LOGGER.debug('{} dealt {} damage to {}'.format(self.avatar, damage_dealt, attacked_avatar))
            if attacked_avatar.health <= 0:
                respawn_location = world_map.get_random_spawn_location()
                attacked_avatar.die(respawn_location)
                world_map.get_cell(self._target_location).avatar = None
                world_map.get_cell(respawn_location).avatar = attacked_avatar
        else:
            self._avatar.add_event(FailedAttackEvent(self._target_location))
        _add_score_from_cell_if_needed(self._avatar, world_map)


# TODO: investigate moving this to after an action is handled - it is not specific to an action
def _add_score_from_cell_if_needed(avatar, world_map):
    cell = world_map.get_cell(avatar.location)
    if cell.generates_score:
        avatar.score += 1

ACTIONS = {
    'attack': AttackAction,
    'move': MoveAction,
    'wait': WaitAction,
}
