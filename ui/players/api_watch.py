from django.http import JsonResponse
from random import randint
from math import pi, sin, cos


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
    return JsonResponse(__world_parameters)



def get_world_state(request):
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
