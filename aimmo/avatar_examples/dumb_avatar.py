class Avatar(object):
    def handle_turn(self, world_state, avatar_state):
        from simulation.action import MoveAction
        import simulation.direction as direction
        import random

        new_dir = random.choice(direction.ALL_DIRECTIONS)
        return MoveAction(new_dir)
