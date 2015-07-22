from django.http import JsonResponse
from random import randint
from math import pi, sin, cos
from simulation.turn_manager import world_state_provider

__world_parameters = {
    "width": 15,
    "height": 15,
    "layout": [
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    ]
}

__world_state = {
    "players": {
        0: {
            "id": "0",
            "x": 2 + randint(0, 1),
            "y": 4,
            "rotation": pi * randint(0, 3) / 2,
            "colours": {
                "bodyStroke": "#f00",
                "bodyFill": "#fbb",
                "eyeStroke": "#faa",
                "eyeFill": "#fee"
            }
        },
        1: {
            "id": "1",
            "x": 6,
            "y": 11,
            "rotation": pi * 0.5,
            "colours": {
                "bodyStroke": "#00f",
                "bodyFill": "#bbf",
                "eyeStroke": "#aaf",
                "eyeFill": "#eef"
            }
        },
        2: {
            "id": "2",
            "x": 3,
            "y": 12,
            "rotation": pi * 1.5,
            "colours": {
                "bodyStroke": "#0ff",
                "bodyFill": "#bff",
                "eyeStroke": "#aff",
                "eyeFill": "#eff"
            }
        }
    },
    "items": [

    ]
}


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
    return {
        'id': avatar.player_id,
        'x': avatar.location.col,
        'y': avatar.location.row,
        'rotation': 0,
        "colours": {
            "bodyStroke": "#0ff",
            "bodyFill": "#bff",
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


def get_world_state_old(request):
    for playerKey in __world_state["players"].keys():
        player = __world_state["players"][playerKey]

        offset_x = int(round(cos(player["rotation"])))
        offset_y = int(round(sin(player["rotation"])))
        new_x = player["x"] + offset_x
        new_y = player["y"] + offset_y

        if (new_x < 0 or new_x >= __world_parameters["width"] or new_y < 0 or new_y >= __world_parameters["height"]
                or __world_parameters["layout"][new_y][new_x] == 1):
            player["rotation"] = randint(0, 3) * pi / 2
        else:
            player["x"] = new_x
            player["y"] = new_y

    return JsonResponse(__world_state)
