class Avatar:
    def handle_turn(self, world_state, avatar_state):
        new_dir = random.choice(direction.ALL_DIRECTIONS)
        return MoveAction(new_dir)
