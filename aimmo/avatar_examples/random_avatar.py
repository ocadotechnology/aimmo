def next_turn(world_state, avatar_state):
    directions = (direction.EAST, direction.SOUTH, direction.WEST, direction.NORTH)
    return MoveAction(random.choice(directions))
