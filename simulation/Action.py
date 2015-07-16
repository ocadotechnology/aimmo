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
            player.location = target_location

class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def apply(self, world_state, player):
        other_player = world_state.get_player_at(player.location + self.direction)
        if other_player:
            pass
        #TODO: add event to send to avatar next turn
        else:
            #TODO: add event to send to avatar next turn
            pass
