import random
from logging import getLogger

LOGGER = getLogger(__name__)


class SpawnLocationFinder:

    def __init__(self, world_map):
        self._world_map = world_map

    def potential_spawn_locations(self):
        """
        Used to make sure that the cell is free before spawning.
        """
        return (c for c in self._world_map.all_cells()
                if c.habitable and not
                c.generates_score and not
                c.avatar and not
                c.pickup)

    def get_random_spawn_locations(self, max_locations):
        if max_locations <= 0:
            return []
        potential_locations = list(self.potential_spawn_locations())
        try:
            return random.sample(potential_locations, max_locations)
        except ValueError:
            return potential_locations

    def get_random_spawn_location(self):
        """Return a single random spawn location.

        Throws:
            IndexError: if there are no possible locations.
        """
        return self.get_random_spawn_locations(1)[0].location
