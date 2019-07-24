def next_turn(world_state, avatar_state):
    avatar_state = avatar_state
    location = avatar_state.location

    directions = (direction.EAST, direction.SOUTH, direction.WEST, direction.NORTH)
    direction_of_other_avatar = next(
        (
            d
            for d in directions
            if world_state.is_visible(location + d)
            and world_state.get_cell(location + d).avatar
        ),
        None,
    )
    if direction_of_other_avatar:
        return AttackAction(direction_of_other_avatar)

    direction_to_other_player = direction_to(
        next(
            cell.location
            for cell in world_state.all_cells()
            if cell.avatar and cell.location != avatar_state.location
        )
    )
    if direction_to_other_player:
        return MoveAction(
            random.choice(directions + ((direction_to_other_player,) * 10))
        )
    return MoveAction(random.choice(directions))


def direction_to(location):
    vector_to = location - location
    if vector_to.x != 0:
        return direction.Direction(1 if vector_to.x > 0 else -1, 0)
    if vector_to.y != 0:
        return direction.Direction(0, 1 if vector_to.y > 0 else -1)
    return None
