from simulation.location import Location
from simulation.direction import NORTH, SOUTH, EAST, WEST


class AvatarView():
    """
    The custom view of the world for each of the avatars. The main
    use of this class is that when the view is moved, the game service
    knows which objects need to be created and which need to be deleted
    from the scene.

    Say the view is 4x4 cells. Cells 'in view' are marked with a 'V'.
                                 _ _ _ _
                               |V V V V V|
                               |V V V V V|
                               |V V V V V|
                               |V_V_V_V_V|
    Now suppose the user moves east. The idea is the following,
                            C C C_C_C_C_C C
                            C C|C V V V V|R
                            C C|C V V V V|R
                            C C|C V V V V|R
                            C C|C_V_V_V_V|R
                            C C C C C C C C
    where C stands for 'clear' and R for 'reveal'. This class calculates
    for every move action the cells to clear and the cells to reveal, and keeps
    track of the cells in view. This reduces the computations of how to change
    the view to only what's strictly necessary. Following with the example, after
    sending the game objects to create/delete in world_state, the new view would be
                                 _ _ _ _
                               |  V V V V|V
                               |  V V V V|V
                               |  V V V V|V
                               | _V_V_V_V|V
    where the original view is delimited by the | and the _.
    """

    def __init__(self, initial_location, radius):
        self.NE_horizon = Location(initial_location.x + radius, initial_location.y + radius)
        self.NW_horizon = Location(initial_location.x - radius, initial_location.y + radius)
        self.SE_horizon = Location(initial_location.x + radius, initial_location.y - radius)
        self.SW_horizon = Location(initial_location.x - radius, initial_location.y - radius)
        self.cells_to_reveal = set([])
        self.cells_to_clear = set([])
        self.cells_in_view = set([])
        self.is_empty = True

    def location_in_view(self, location):
        return location.x >= self.NW_horizon.x and \
               location.y <= self.NW_horizon.y and \
               location.x <= self.SE_horizon.x and \
               location.y >= self.SE_horizon.y

    # Returns all the cells in the rectangle defined by two corners.
    @classmethod
    def cells_in_rectangle(self, top_left, bottom_right, world_map):
        cells = set([])
        for x in xrange(max(top_left.x, world_map.min_x()), min(bottom_right.x, world_map.max_x() + 1)):
            for y in xrange(max(bottom_right.y, world_map.min_y()), min(top_left.y, world_map.max_y() + 1)):
                cells.add(world_map.get_cell(Location(x, y)))
        return cells

    # Reveals all the cells in the view.
    def reveal_all_cells(self, world_map):
        self.cells_to_reveal = self.cells_in_rectangle(self.NW_horizon, self.SE_horizon, world_map)
        self.cells_in_view = set(self.cells_to_reveal)

    def move(self, move_direction, world_map):
        self.cells_to_clear = set([])
        # Update cells to clear and to reveal depending on the move direction.
        if move_direction == EAST:
            self.cells_to_clear |= self.cells_in_rectangle(self.NW_horizon + WEST + WEST + NORTH,
                                                           self.SW_horizon + EAST + SOUTH,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.NW_horizon + EAST + NORTH,
                                                           self.NE_horizon,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.SW_horizon + EAST,
                                                           self.SE_horizon + SOUTH,
                                                           world_map)

            self.cells_to_reveal = self.cells_in_rectangle(self.NE_horizon,
                                                           self.SE_horizon + EAST,
                                                           world_map)
        elif move_direction == WEST:
            self.cells_to_clear |= self.cells_in_rectangle(self.NE_horizon + WEST + NORTH,
                                                           self.SE_horizon + EAST + EAST + SOUTH,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.NW_horizon + NORTH,
                                                           self.NE_horizon + WEST,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.SW_horizon,
                                                           self.SE_horizon + WEST + SOUTH,
                                                           world_map)

            self.cells_to_reveal = self.cells_in_rectangle(self.NW_horizon + WEST,
                                                           self.SW_horizon,
                                                           world_map)
        elif move_direction == NORTH:
            self.cells_to_clear |= self.cells_in_rectangle(self.SW_horizon + WEST + NORTH,
                                                           self.SE_horizon + EAST + SOUTH + SOUTH,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.NW_horizon + WEST,
                                                           self.SW_horizon + NORTH,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.NE_horizon,
                                                           self.SE_horizon + EAST + NORTH,
                                                           world_map)

            self.cells_to_reveal = self.cells_in_rectangle(self.NW_horizon + NORTH,
                                                           self.NE_horizon,
                                                           world_map)
        elif move_direction == SOUTH:
            self.cells_to_clear |= self.cells_in_rectangle(self.NW_horizon + WEST + NORTH + NORTH,
                                                           self.NE_horizon + EAST + SOUTH,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.NW_horizon + WEST + SOUTH,
                                                           self.SW_horizon,
                                                           world_map)
            self.cells_to_clear |= self.cells_in_rectangle(self.NE_horizon + SOUTH,
                                                           self.SE_horizon + EAST,
                                                           world_map)

            self.cells_to_reveal = self.cells_in_rectangle(self.SW_horizon,
                                                           self.SE_horizon + SOUTH,
                                                           world_map)

        # Update cells in view. (Note that these are set operations: union and set difference)
        self.cells_in_view |= self.cells_to_reveal
        self.cells_in_view -= self.cells_to_clear

        # Shift the four view corners (horizons).
        self.NE_horizon += move_direction
        self.NW_horizon += move_direction
        self.SE_horizon += move_direction
        self.SW_horizon += move_direction
        