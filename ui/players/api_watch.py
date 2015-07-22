import random
from django.http import JsonResponse
from simulation.turn_manager import world_state_provider


def get_world_parameters(request):
    world = world_state_provider.lock_and_get_world()
    try:
        response = JsonResponse({
            "width": 15,
            "height": 15,
            "layout": [[x.key for x in y] for y in world.world_map.grid.tolist()]
        }, safe=False)
    finally:
        world_state_provider.release_lock()
    return response


def player_dict(avatar):
    # TODO: implement better colour functionality: will eventually fall off end of numbers
    colour = "#%06x" % (avatar.player_id * 929)
    return {
        'id': avatar.player_id,
        'x': avatar.location.col,
        'y': avatar.location.row,
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
