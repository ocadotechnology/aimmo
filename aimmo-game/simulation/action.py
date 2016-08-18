from logging import getLogger
from simulation.direction import Direction
from simulation.event import FailedAttackEvent, FailedMoveEvent, MovedEvent, PerformedAttackEvent, ReceivedAttackEvent

LOGGER = getLogger(__name__)


class Action(object):
    def __init__(self, avatar):
        self._avatar = avatar
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

    def register(self, world_map):
        if world_map.is_on_map(self.target_location):
            world_map.get_cell(self.target_location).actions.append(self)

    def process(self, world_map):
        if self.is_legal(world_map):
            self.apply(world_map)
        else:
            self.reject()

    def is_legal(self, world_map):
        raise NotImplementedError('Abstract method')

    def apply(self, world_map):
        raise NotImplementedError('Abstract method')

    def reject(self):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def __init__(self, avatar):
        super(WaitAction, self).__init__(avatar)

    def is_legal(self, world_map):
        return True

    def apply(self, world_map):
        self.avatar.clear_action()


class MoveAction(Action):
    def __init__(self, avatar, direction):
        # Untrusted data!
        self.direction = Direction(**direction)
        super(MoveAction, self).__init__(avatar)

    def is_legal(self, world_map):
        return world_map.can_move_to(self.target_location)

    def process(self, world_map):
        self.chain(world_map, {self.avatar.location})

    def apply(self, world_map):
        event = MovedEvent(self.avatar.location, self.target_location)
        self.avatar.add_event(event)

        world_map.get_cell(self.avatar.location).avatar = None
        self.avatar.location = self.target_location
        world_map.get_cell(self.target_location).avatar = self.avatar
        self.avatar.clear_action()
        return True

    def chain(self, world_map, visited):
        if not self.is_legal(world_map):
            return self.reject()

        # Detect cycles
        if self.target_location in visited:
            return self.reject()

        next_cell = world_map.get_cell(self.target_location)
        if not next_cell.is_occupied:
            return self.apply(world_map)

        next_action = next_cell.avatar.action
        if next_action.chain(world_map, visited | {self.target_location}):
            return self.apply(world_map)

        return self.reject()

    def reject(self):
        event = FailedMoveEvent(self.avatar.location, self.target_location)
        self.avatar.add_event(event)
        self.avatar.clear_action()
        return False


class AttackAction(Action):
    def __init__(self, avatar, direction):
        # Untrusted data!
        self.direction = Direction(**direction)
        super(AttackAction, self).__init__(avatar)

    def is_legal(self, world_map):
        return True if world_map.attackable_avatar(self.target_location) else False

    def apply(self, world_map):
        attacked_avatar = world_map.attackable_avatar(self.target_location)
        damage_dealt = 1
        self.avatar.add_event(PerformedAttackEvent(attacked_avatar,
                                                   self.target_location,
                                                   damage_dealt))
        attacked_avatar.add_event(ReceivedAttackEvent(self.avatar,
                                                      damage_dealt))
        attacked_avatar.damage(damage_dealt)

        LOGGER.debug('{} dealt {} damage to {}'.format(self.avatar,
                                                       damage_dealt,
                                                       attacked_avatar))
        self.avatar.clear_action()

        if attacked_avatar.health <= 0:
            # Move responsibility for this to avatar.die() ?
            respawn_location = world_map.get_random_spawn_location()
            attacked_avatar.die(respawn_location)
            world_map.get_cell(self.target_location).avatar = None
            world_map.get_cell(respawn_location).avatar = attacked_avatar

    def reject(self):
        self.avatar.add_event(FailedAttackEvent(self.target_location))
        self.avatar.clear_action()

ACTIONS = {
    'attack': AttackAction,
    'move': MoveAction,
    'wait': WaitAction,
}

PRIORITIES = {
    WaitAction: 0,
    AttackAction: 1,
    MoveAction: 2,
}
