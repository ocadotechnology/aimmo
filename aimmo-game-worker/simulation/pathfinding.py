# Inspired by https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# and https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc

from warnings import warn
import heapq

from .location import Location
from .direction import ALL_DIRECTIONS


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, cell=None):
        self.parent = parent
        self.cell = cell

        self.g = 0  # g is the distance between the current node and the start node
        self.h = 0  # h is the heuristic - estimated distance from the current node to the end node
        self.f = 0  # f is the total cost of the node (g + h)

    @property
    def location(self):
        return self.cell.location

    def __eq__(self, other):
        return self.location == other.location

    def __repr__(self):
        return f"{self.location} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
        return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
        return self.f > other.f


def _get_adjacent_cells(current_node, world_map):
    adj = []
    # we move only in 4 directions
    for direction in ALL_DIRECTIONS:
        # make sure the cell is within the grid
        try:
            tx = current_node.location.x + direction.x
            ty = current_node.location.y + direction.y
            cell = world_map.get_cell(Location(tx, ty))
        except KeyError:
            cell = None
        # Make sure walkable cell
        if cell and cell.habitable:
            adj.append(cell)
    return adj


def _constructed_path(current_node):
    # follow backwards from current node all the way to the start
    path = []
    current = current_node
    while current is not None:
        path.append(current.cell)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(world_map, start_cell, end_cell):
    """
    Returns a list of Cell as a path from the given start to the given end in the given world_map.
    The best path navigates the obstacles (but not other avatars, as they're assumed to be moving).
    For explanation of the A* pathfinding, see the medium post at the top.
    """

    # Create start and end node
    start_node = Node(None, start_cell)
    end_node = Node(None, end_cell)

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Loop until you find the goal or exhaust the nodes
    while len(open_list) > 0:

        # look for the lowest F cost square on the open list for current node (returned by the heapq)
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal!
        if current_node == end_node:
            return _constructed_path(current_node)

        # Generate children
        children = []
        for acell in _get_adjacent_cells(current_node, world_map):
            new_node = Node(current_node, acell)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            # calculate the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.location.x - end_node.location.x) ** 2) + (
                (child.location.y - end_node.location.y) ** 2
            )
            child.f = child.g + child.h

            # check if it is already in the open list, and if this path to that square is better,
            # using G cost as the measure (lower G is better)
            open_nodes = [
                open_node
                for open_node in open_list
                if (child.location == open_node.location and child.g > open_node.g)
            ]
            if len(open_nodes) > 0:
                continue

            # add the child to the open list
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None
