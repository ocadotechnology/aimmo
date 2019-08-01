def next_turn(world_state, avatar_state):
    world_state = world_state
    avatar_state = avatar_state

    if world_state.get_cell(avatar_state.location).generates_score:
        return WaitAction()

    possible_directions = get_possible_directions()
    directions_to_emphasise = [
        d for d in possible_directions if is_towards(d, get_closest_pickup_location())
    ]
    return MoveAction(
        random.choice(possible_directions + (directions_to_emphasise * 5))
    )


def is_towards(direction, location):
    if location:
        return distance_between(avatar_state.location, location) > distance_between(
            avatar_state.location + direction, location
        )
    else:
        return None


def distance_between(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_closest_pickup_location(self):
    pickup_cells = list(world_state.pickup_cells())
    if pickup_cells:
        c = min(
            pickup_cells,
            key=lambda cell: distance_between(cell.location, avatar_state.location),
        )
        print("targetting" + c)
        return c.location
    else:
        return None


def get_possible_directions():
    directions = (direction.EAST, direction.SOUTH, direction.WEST, direction.NORTH)
    return [d for d in directions if world_state.can_move_to(avatar_state.location + d)]
