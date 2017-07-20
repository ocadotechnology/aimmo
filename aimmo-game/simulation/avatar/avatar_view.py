from .. import direction, location

class AvatarView():
    """
    The personalized veiw of the world for each avatar. The main
    use of this class is that when the view is moved, the game service
    knows which objects need to be created and which need to be deleted
    from the scene.
    """

    def __init__(self, initial_location, radius):
        self.NE_horizon = location.Location(initial_location.x + radius, initial_location.y + radius)
        self.NW_horizon = location.Location(initial_location.x - radius, initial_location.y + radius)
        self.SE_horizon = location.Location(initial_location.x + radius, initial_location.y - radius)
        self.SW_horizon = location.Location(initial_location.x - radius, initial_location.y - radius)
        self.cells_to_reveal = {}
        self.cells_to_clear = {}
        self.is_empty = True

    # Returns all the cells in the rectangle defined by two corners.
    def cells_in_rectangle(sefl, top_left, bottom_right, world_map):
        cells = []
        for x in range(top_left.x, bottom_right.x):
            for y in range(bottom_right.y, top_left.y):
                cells.append(world_map.get_cell_by_coords(x, y))
        return cells

    # Reveals all the cells in the view.
    def reveal_all_cells(self):
        self.cells_to_reveal = self.cells_in_rectangle(self.NW_horizon, self.SE_horizon)

    def move(self, move_direction, world_map):
        # Shift the four view corners (horizons).
        def move_horizons(direction):
            self.NE_horizon += direction
            self.NW_horizon += direction
            self.SE_horizon += direction
            self.SW_horizon += direction

        # Update cells to clear and to reveal depending on the move direction.
        if move_direction == direction.EAST:
            self.cells_to_clear = self.cells_in_rectangle(self.NW_horizon, self.SW_horizon + direction.EAST, world_map)
            self.cells_to_reveal = self.cells_in_rectangle(self.NE_horizon, self.SE_horizon + direction.EAST, world_map)
        elif move_direction == direction.WEST:
            self.cells_to_clear = self.cells_in_rectangle(self.NE_horizon + direction.WEST, self.SE_horizon, world_map)
            self.cells_to_reveal = self.cells_in_rectangle(self.NW_horizon + direction.WEST, self.SW_horizon, world_map)
        elif move_direction == direction.NORTH:
            self.cells_to_clear = self.cells_in_rectangle(self.SW_horizon + direction.NORTH, self.SE_horizon, world_map)
            self.cells_to_reveal = self.cells_in_rectangle(self.NW_horizon + direction.NORTH, self.NE_horizon,world_map)
        elif move_direction == direction.SOUTH:
            self.cells_to_clear = self.cells_in_rectangle(self.NW_horizon, self.NE_horizon + direction.SOUTH, world_map)
            self.cells_to_reveal = self.cells_in_rectangle(self.SW_horizon, self.SE_horizon + direction.SOUTH, world_map)
        else:
            raise ValueError

        move_horizons(move_direction)