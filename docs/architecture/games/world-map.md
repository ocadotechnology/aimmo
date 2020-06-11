# World Map

The World Map is the central component of the simulation. The class itself consists of a grid and a set of JSON settings. The grid consists of a dictionary of type <Location, Cell>.

### Cells

A cell has the following components:

- location - (x, y) pairs that can be added together, serialized, compared, etc.
- avatars - see [Game Objects](game-objects) for more details
- pickup - see [Game Objects](game-objects) for more details
- cell content - the cell content can either be a score cell, an obstacle or a plain floor cell
- actions - an array where the intended actions of different avatars are registered and, afterwards, applied

### World Map basic functionality

World Map has a lot of misc functionality, as multiple other objects communicate with it and need a simple API.

Cell specific functionality:

- get_cell
- all_cells
- score_cells
- pickup_cells

Map dimension functionality:

- is_on_map
- max_x
- max_y
- min_x
- min_y
- num_cols
- num_rows
- num_cells

### The Update Cycle

The most important responsibility of the world map class is the `self.update` after the intended character moves have been recorded by the Simulation Runner. The function `update` is called by the [Simulation Runner](simulation-runner).

The update cycle is as follows:

- update avatars
  - apply score: each avatar received a score
  - apply pickups: each avatar grabs a pickup if present
- update map:
  - expand the map so that it fits the size of the avatars if more avatars arrive
  - reset score locations: new score locations are generated
  - add pickups: new pickups are generated

All the map updates are regulated using the settings of a map. Some useful settings fields are:

- TARGET_NUM_CELLS_PER_AVATAR - regulates the size of the map by number of avatars
- TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR - used to regulate the number of score locations; the new score locations are generated randomly and added to the map
- SCORE_DESPAWN_CHANCE - another parameter to regulate the score cells generation; the game is more dynamic as some score cells are getting removed each turn and new ones are generated, giving the player the impressing of score cells moving around
- TARGET_NUM_PICKUPS_PER_AVATAR - regulate the number of pickups similarly to how the number of score locations are regulated
- PICKUP_SPAWN_CHANCE - a regulation parameter similar to SCORE_DESPAWN_CHANCE

[simulation-runner]: simulation-runner.md
