from django.http import JsonResponse
from simulation.location import Location
from simulation.turn_manager import world_state_provider
from simulation.world_map import Cell
from django.core.serializers.json import DjangoJSONEncoder


def to_cell_type(cell):
    if not cell.habitable:
        return "WALL"
    if cell.generates_score:
        return "SCORE"
    return "GRASS"


def player_dict(avatar):
    return {
        'id': avatar.player_id,
        'x': avatar.location.x,
        'y': avatar.location.y,
        'health': avatar.health,
        'score': avatar.score,
        'customization': hash(avatar.player_id) % 25,
        'lastMove': avatar.last_move.name if avatar.last_move else None
    }


def get_world_state(request):
    try:
        world = world_state_provider.lock_and_get_world()
        num_cols = len(world.world_map.grid)
        num_rows = len(world.world_map.grid[0])
        grid = [[None for x in xrange(num_cols)] for y in xrange(num_rows)]
        for cell in world.world_map.all_cells:
            grid[cell.location.x][cell.location.y] = to_cell_type(cell)
        # TODO is the ID always a number? Can this be an array?
        player_data = {p.player_id: player_dict(p) for p in world.avatar_manager.avatarsById.values()}
        return JsonResponse({
            'players': player_data,
            'score_locations': [(cell.location.x, cell.location.y) for cell in world.world_map.generate_score_cells()],
            'pickup_locations': [(cell.location.x, cell.location.y) for cell in world.world_map.generate_pickup_cells()],

            'map_changed': True,  # TODO: experiment with only sending deltas (not if not required)
            'width': num_cols,
            'height': num_rows,
            'layout': grid,
        })
    finally:
        world_state_provider.release_lock()
