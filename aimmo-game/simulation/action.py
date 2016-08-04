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
        if world_map.is_on_map(self._target_location):
            world_map.get_cell(self._target_location).actions.append(self)

    def apply_if_legal(self, world_map):
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
        pass


class MoveAction(Action):
    def __init__(self, avatar, direction):
        # Untrusted data!
        self.direction = Direction(**direction)
        super(MoveAction, self).__init__(avatar)

    def is_legal(self, world_map):
        return world_map.can_move_to(self._target_location)

    def apply(self, world_map):
        event = MovedEvent(self._avatar.location, self._target_location)
        self._avatar.add_event(event)

        world_map.get_cell(self._avatar.location).avatar = None
        self._avatar.location = self._target_location
        world_map.get_cell(self._target_location).avatar = self._avatar

        new_cell = world_map.get_cell(self._target_location)
        if new_cell.pickup:
            # TODO:  extract pickup logic into pickup when adding multiple types
            self._avatar.health = min(10, self._avatar.health + new_cell.pickup.health_restored)
            new_cell.pickup = None

    def chain(self, world_map, first):
        if self.is_legal(world_map):
            avatar = world_map.get_cell(self.target_location).avatar
            move = avatar.action
            if avatar is None or (move is not first and move.chain(world_map, first)):
                self.apply(world_map)
                self.avatar.clear_action()
                return True

        self.reject()
        self.avatar.clear_action()
        return False

    def reject(self):
        event = FailedMoveEvent(self._avatar.location, self._target_location)
        self._avatar.add_event(event)


class AttackAction(Action):
    def __init__(self, avatar, direction):
        # Untrusted data!
        self.direction = Direction(**direction)
        super(AttackAction, self).__init__(avatar)

    def is_legal(self, world_map):
        return True if world_map.attackable_avatar(self._target_location) else False

    def apply(self, world_map):
        attacked_avatar = world_map.attackable_avatar(self._target_location)
        damage_dealt = 1
        self._avatar.add_event(PerformedAttackEvent(attacked_avatar,
                                                    self._target_location,
                                                    damage_dealt))
        attacked_avatar.add_event(ReceivedAttackEvent(self._avatar,
                                                      damage_dealt))
        attacked_avatar.health -= damage_dealt

        LOGGER.debug('{} dealt {} damage to {}'.format(self._avatar,
                                                       damage_dealt,
                                                       attacked_avatar))

        if attacked_avatar.health <= 0:
            # Move responsibility for this to avatar.die() ?
            respawn_location = world_map.get_random_spawn_location()
            attacked_avatar.die(respawn_location)
            world_map.get_cell(self._target_location).avatar = None
            world_map.get_cell(respawn_location).avatar = attacked_avatar

    def reject(self):
        self._avatar.add_event(FailedAttackEvent(self._target_location))

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
