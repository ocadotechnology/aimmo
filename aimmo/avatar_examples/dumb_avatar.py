class Avatar(object):
    def handle_turn(self, world_map, avatar_state):
        from simulation.action import MoveAction
        from simulation.direction import ALL_DIRECTIONS
        import random

        return MoveAction(random.choice(ALL_DIRECTIONS))
