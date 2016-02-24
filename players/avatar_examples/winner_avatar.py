from simulation.action import MoveAction
from simulation import direction


class Avatar(object):
    def handle_turn(self, world_state, events):
        import random
        from simulation.action import WaitAction
        
        self.world_state = world_state
        
        if world_state.map_centred_at_me.get_cell(world_state.my_avatar.location).generates_score:
            return WaitAction()
        
        possible_directions = self.get_possible_directions()
        directions_to_emphasise = [d for d in possible_directions if self.is_towards(d, self.get_closest_score_location())]
        return MoveAction(random.choice(possible_directions + (directions_to_emphasise * 5)))
        
    def is_towards(self, direction, location):
        return self.distance_between(self.world_state.my_avatar.location, location) > \
            self.distance_between(self.world_state.my_avatar.location + direction, location)
            
    def distance_between(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)
        
    def get_closest_score_location(self):
        return min(self.world_state.map_centred_at_me.score_cells(), key=lambda cell: self.distance_between(cell.location, self.world_state.my_avatar.location)).location

    def get_possible_directions(self):
        from simulation.direction import ALL_DIRECTIONS

        return [d for d in ALL_DIRECTIONS if self.world_state.map_centred_at_me.can_move_to(self.world_state.my_avatar.location + d)]
