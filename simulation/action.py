from event import *


class Action(object):
    def apply(self, world_state, player):
        raise NotImplementedError('Abstract method')


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, player):
        current_location = player.location
        target_location = current_location + self.direction
        if world_state.world_map.can_move_to(target_location):
            player.add_event(MovedEvent(player.location, target_location))
            player.location = target_location
        else:
            player.add_event(MovedEvent(player.location, target_location))


class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, player):
        target_location = player.location + self.direction
        attacked_players = world_state.get_players_at(target_location)
        if attacked_players:
            for other_player in attacked_players:
                damage_dealt = 1
                player.add_event(PerformedAttackEvent(other_player, target_location, damage_dealt))
                other_player.add_event(ReceivedAttackEvent(player, damage_dealt))
        else:
            player.add_event(FailedAttackEvent(target_location))
