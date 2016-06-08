from simulation.world_map import WorldMap
from simulation.location import Location


def apply_fog_of_war(world_map, avatar_wrapper):
    """
    Takes a world state and an avatar and returns a personalised view of the world.
    :param world_map: the state of the game
    :param avatar_wrapper: the application's view of the avatar
    :return: a world state tailored to the given avatar
    """

    location = avatar_wrapper.location
    no_fog_distance = avatar_wrapper.fog_of_war_modifier + world_map.get_no_fog_distance()
    #partial_fog_distance = avatar_wrapper.fog_of_war_modifier + world_map.get_partial_fog_distance()

    lower_x = max(location.x - no_fog_distance, 0)
    lower_y = max(location.y - no_fog_distance, 0)
    upper_x = min(location.x + no_fog_distance, len(world_map.grid) - 1)
    upper_y = min(location.y + no_fog_distance, len(world_map.grid[0]) - 1)

    x_diff = upper_x - lower_x
    y_diff = upper_y - lower_y
    grid = [[None for y in range(y_diff + 1)] for x in range(x_diff + 1)]
    for x in range(x_diff + 1):
        for y in range(y_diff + 1):

            cell_location = Location(x + lower_x, y + lower_y)
            if world_map.is_on_map(cell_location):
                grid[x][y] = world_map.get_cell(cell_location)
    return WorldMap(grid)

#def partially_fog_cell(cell):
#    return Cell(cell.location, True, cell.generates_score, None, None)