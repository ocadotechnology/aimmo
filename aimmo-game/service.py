#!/usr/bin/env python
import logging

from simulation.turn_manager import world_state_provider

from simulation import map_generator
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.turn_manager import TurnManager

from threading import Thread
import os

import flask
from flask.ext.cors import CORS
app = flask.Flask(__name__)
CORS(app)


def to_cell_type(cell):
    if not cell.habitable:
        return 1
    if cell.generates_score:
        return 2
    return 0


def player_dict(avatar):
    # TODO: implement better colour functionality: will eventually fall off end of numbers
    colour = "#%06x" % (avatar.player_id * 4999)
    return {
        'id': avatar.player_id,
        'x': avatar.location.x,
        'y': avatar.location.y,
        'health': avatar.health,
        'score': avatar.score,
        'rotation': 0,
        "colours": {
            "bodyStroke": "#0ff",
            "bodyFill": colour,
            "eyeStroke": "#aff",
            "eyeFill": "#eff",
        }
    }


@app.route('/')
def get_world_state():
    try:
        world = world_state_provider.lock_and_get_world()
        num_cols = len(world.world_map.grid)
        num_rows = len(world.world_map.grid[0])
        grid = [[None for x in xrange(num_cols)] for y in xrange(num_rows)]
        for cell in world.world_map.all_cells():
            grid[cell.location.x][cell.location.y] = to_cell_type(cell)
        player_data = {p.player_id: player_dict(p) for p in world.avatar_manager.avatars}
        return flask.jsonify(**{
            'players': player_data,
            'score_locations': [(cell.location.x, cell.location.y) for cell in world.world_map.score_cells()],
            'pickup_locations': [(cell.location.x, cell.location.y) for cell in world.world_map.pickup_cells()],
            'map_changed': True,  # TODO: experiment with only sending deltas (not if not required)
            'width': num_cols,
            'height': num_rows,
            'layout': grid,
        })
    finally:
        world_state_provider.release_lock()


def run_game():
    print("Running game...")
    my_map = map_generator.generate_map(15, 15, 0.1)
    player_manager = AvatarManager([])
    game_state = GameState(my_map, player_manager)
    turn_manager = TurnManager(game_state)

    turn_manager.run_game()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    thread = Thread(target=run_game)
    thread.daemon = True
    thread.start()
    app.config['DEBUG'] = True
    app.run()
