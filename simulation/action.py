from event import *


class Action(object):
    def apply(self, world_state, avatar):
        raise NotImplementedError('Abstract method')


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, avatar):
        current_location = avatar.location
        target_location = current_location + self.direction
        if world_state.world_map.can_move_to(target_location):
            avatar.add_event(MovedEvent(avatar.location, target_location))
            avatar.location = target_location
        else:
            avatar.add_event(MovedEvent(avatar.location, target_location))


class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, avatar):
        target_location = avatar.location + self.direction
        attacked_avatars = world_state.get_avatars_at(target_location)
        if attacked_avatars:
            for other_avatar in attacked_avatars:
                damage_dealt = 1
                avatar.add_event(PerformedAttackEvent(
                    other_avatar, target_location, damage_dealt))
                other_avatar.add_event(
                    ReceivedAttackEvent(avatar, damage_dealt))
        else:
            avatar.add_event(FailedAttackEvent(target_location))
