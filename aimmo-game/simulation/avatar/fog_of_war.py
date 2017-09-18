import copy

from simulation.location import Location
from simulation.world_map import WorldMap


def apply_fog_of_war(world_map, avatar_wrapper):
    """
    Takes a world state and an avatar and returns a personalised view of the world.
    :param world_map: the state of the game
    :param avatar_wrapper: the application's view of the avatar
    :return: a world state tailored to the given avatar
    """

    location = avatar_wrapper.location
    no_fog_distance = avatar_wrapper.fog_of_war_modifier + world_map.get_no_fog_distance()
    partial_fog_distance = avatar_wrapper.fog_of_war_modifier + world_map.get_partial_fog_distance()

    lower_x = max(location.x - partial_fog_distance, world_map.min_x())
    lower_y = max(location.y - partial_fog_distance, world_map.min_y())
    upper_x = min(location.x + partial_fog_distance, world_map.max_x())
    upper_y = min(location.y + partial_fog_distance, world_map.max_y())

    grid = {}
    for x in range(lower_x, upper_x + 1):
        for y in range(lower_y, upper_y + 1):
            cell_location = Location(x, y)
            if world_map.is_on_map(cell_location):
                x_dist = abs(cell_location.x - location.x)
                y_dist = abs(cell_location.y - location.y)
                if should_partially_fog(no_fog_distance, partial_fog_distance, x_dist, y_dist):
                    grid[location] = partially_fog_cell(world_map.get_cell(cell_location))
                else:
                    grid[location] = world_map.get_cell(cell_location)
    return WorldMap(grid, world_map.settings)


def should_partially_fog(no_fog_distance, partial_fog_distance, x_dist, y_dist):
    # TODO: partial_fog_distance implemented in this method somehow.
    return x_dist > no_fog_distance or y_dist > no_fog_distance


def partially_fog_cell(cell):
    partially_fogged_cell = copy.deepcopy(cell)
    partially_fogged_cell.habitable = True
    partially_fogged_cell.avatar = None
    partially_fogged_cell.pickup = None
    partially_fogged_cell.partially_fogged = True
    return partially_fogged_cell
