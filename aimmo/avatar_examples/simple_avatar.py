class Avatar:
    def next_turn(self, world_state, avatar_state):
        return MoveAction(direction.NORTH)
