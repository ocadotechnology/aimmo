from event import *


class Action(object):
    def apply(self, world_state, avatar):
        raise NotImplementedError('Abstract method')


class WaitAction(Action):
    def apply(self, world_state, avatar):
        pass


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, avatar):
        target_location = avatar.location + self.direction
        if world_state.world_map.can_move_to(target_location):
            avatar.add_event(MovedEvent(avatar.location, target_location))
            avatar.location = target_location
        else:
            avatar.add_event(FailedMoveEvent(avatar.location, target_location))


class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, avatar):
        target_location = avatar.location + self.direction
        attacked_avatar = world_state.avatar_manager.get_avatar_at(target_location)
        if attacked_avatar:
            damage_dealt = 1
            avatar.add_event(PerformedAttackEvent(attacked_avatar, target_location, damage_dealt))
            attacked_avatar.add_event(ReceivedAttackEvent(avatar, damage_dealt))
            attacked_avatar.health -= damage_dealt
            print attacked_avatar.health  # TODO: if <= 0, kill and respawn
        else:
            avatar.add_event(FailedAttackEvent(target_location))
