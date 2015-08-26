from django.http import JsonResponse
from simulation.turn_manager import world_state_provider


# TODO: rename to something more djangoey or merge with views.py

def to_cell_type(cell):
    if not cell.can_move_to:
        return 1
    if cell.generates_score:
        return 2
    return 0


def get_world_parameters(request):
    world = world_state_provider.lock_and_get_world()
    try:
        num_cols = len(world.world_map.grid)
        num_rows = len(world.world_map.grid[0])
        grid = [[None for x in xrange(num_cols)] for y in xrange(num_rows)]
        for cell in world.world_map.all_cells:
            grid[cell.location.x][cell.location.y] = to_cell_type(cell)
        response = JsonResponse({
            "width": 15,
            "height": 15,
            "layout": grid,
        }, safe=False)
    finally:
        world_state_provider.release_lock()
    return response


def player_dict(avatar):
    # TODO: implement better colour functionality: will eventually fall off end of numbers
    colour = "#%06x" % (avatar.player_id * 929)
    return {
        'id': avatar.player_id,
        'x': avatar.location.x,
        'y': avatar.location.y,
        'health': avatar.health,
        'rotation': 0,
        "colours": {
            "bodyStroke": "#0ff",
            "bodyFill": colour,
            "eyeStroke": "#aff",
            "eyeFill": "#eff"
            }
        }


def get_world_state(request):
    world = world_state_provider.lock_and_get_world()

    player_data = {p.player_id: player_dict(p) for p in world.avatar_manager.avatarsById.values()}

    data = {'players': player_data}
    try:
        response = JsonResponse(data)
    finally:
        world_state_provider.release_lock()
    return response
