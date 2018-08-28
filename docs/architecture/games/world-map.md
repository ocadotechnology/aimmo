# World Map

---

The World Map is the central component of the simulation. The class itself consists of a grid and a set of JSON settings. The grid consists of a dictionary of type <Location, Cell>.

### Cells

A cell has the following components:
* location - (x, y) pairs that can be added together, serialized, compared, etc.
* avatars - see [Game Objects](game-objects) for more details
* pickup - see [Game Objects](game-objects) for more details
* cell content - the cell content can either be a score cell, an obstacle or a plain floor cell
* actions - an array where the intended actions of different avatars are registered and, afterwards, applied

### World Map basic functionality 

World Map has a lot of misc functionality, as multiple other objects communicate with it and need a simple API. 

Cell specific functionality:
* get_cell
* all_cells
* score_cells
* pickup_cells

Map dimension functionality:
* is_on_map
* max_x
* max_y
* min_x
* min_y
* num_cols
* num_rows
* num_cells

### The Update Cycle 

The most important responsibility of the world map class is the `self.update` after the intended character moves have been recorded by the turn manager. The function `udpate` is called by the [Turn Manager](turn-manager). 

_This functionality is quite broad and could be considered for refactoring in a different class._

The update cycle is as follows:
* update avatars
   * apply score: each avatar received a score
   * apply pickups: each avatar grabs a pickup if present
* update map:
   * expand the map so that it fits the size of the avatars if more avatars arrive
   * reset score locations: new score locations are generated
   * add pickups: new pickups are generated

All the map updates are regulated using the settings of a map. Some useful settings fields are:
* TARGET_NUM_CELLS_PER_AVATAR - probably the most important setting for a map; it regulates the size of the map by number of avatars; to make the map static, we override it for the [levels](Levels)
* TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR - used to regulate the number of score locations; the new score locations are generated randomly and added to the map
* SCORE_DESPAWN_CHANCE - another parameter to regulate the score cells generation; the game is more dynamic as some score cells are getting removed each turn and new ones are generated, giving the player the impressing of score cells moving around
* TARGET_NUM_PICKUPS_PER_AVATAR - regulate the number of pickups similarly to how the number of score locations are regulated
* PICKUP_SPAWN_CHANCE - a regulation parameter similar to SCORE_DESPAWN_CHANCE

All of these settings should be overridden in a level to fit the needs of the level design. More documentation on levels can be found [here](levels). 

## Dependencies and other functionality

Dependencies:
* update - used by TurnManager to update the world at each frame
* clear_cell_actions - used by TurnManager to tell WorldMap to clear actions
* cells_to_create - used by WorldState to retreive the cells to view; used to know when to instantiate objects in the scene

Misc:   
* get_random_spawn_location - get a free habitable cell or IndexError
* can_move_to - assert if avatar can move to location
* attackable_avatar - return the avatar attackable at the given location, or None

Most of the misc functions generate coupling with many other classes, making this class reasonably hard to decouple. 
