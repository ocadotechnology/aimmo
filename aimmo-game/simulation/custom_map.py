import abc
import math

from simulation.levels.levels import LEVELS
from pprint import pprint

from simulation.location import Location
from simulation.game_state import GameState
from simulation.world_map import WorldMap
from simulation.world_map import WorldMapStaticSpawnDecorator
from simulation.world_map import DEFAULT_LEVEL_SETTINGS
from simulation.world_map import Cell

""" Custom level generation. TODO: document @ custom_map, map_generator """

class BaseGenerator(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, settings):
        self.settings = settings

    def get_game_state(self, avatar_manager):
        return GameState(self.get_map(), avatar_manager, self.check_complete)

    def check_complete(self, game_state):
        return False

    @abc.abstractmethod
    def get_map(self):
        pass

class EmptyMapGenerator(BaseGenerator):
    def __init__(self, settings):
        self.height =  self.settings['START_HEIGHT']
        self.width = self.settings['START_WIDTH']
        self.settings = settings

    def __init__(self, height, width, settings):
        self.height = height
        self.width = width
        self.settings = settings

    def get_map(self):
        def _min_max_from_dimensions(height, width):
            max_x = int(math.floor(width / 2))
            min_x = -(width - max_x - 1)
            max_y = int(math.floor(height / 2))
            min_y = -(height - max_y - 1)
            return min_x, max_x, min_y, max_y

        new_settings = DEFAULT_LEVEL_SETTINGS.copy()
        new_settings.update(self.settings)

        (min_x, max_x, min_y, max_y) = _min_max_from_dimensions(self.height, self.width)
        grid = {}
        for x in xrange(min_x, max_x + 1):
            for y in xrange(min_y, max_y + 1):
                location = Location(x, y)
                grid[location] = Cell(location)
        return WorldMap(grid, new_settings)

class BaseLevelGenerator(BaseGenerator):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(BaseLevelGenerator, self).__init__(*args, **kwargs)
        self.settings.update(DEFAULT_LEVEL_SETTINGS)

class TemplateLevelGenerator(BaseLevelGenerator):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(TemplateLevelGenerator, self).__init__(*args, **kwargs)
        self.settings.update(DEFAULT_LEVEL_SETTINGS)

################################################################################

class Decoder():
    __metaclass__ = abc.ABCMeta

    def __init__(self, code):
        self.code = code

    @abc.abstractmethod
    def decode(self, json, world_map):
        pass

class ScoreCellDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        world_map = WorldMapStaticSpawnDecorator(world_map, Location(x, y))
        world_map.get_cell(Location(x, y)).generates_score = True

class ObstacleDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        world_map.get_cell(Location(x, y)).habitable = False

################################################################################

class JsonLevelGenerator(TemplateLevelGenerator):
    def _register_json(self, json_map):
        self.json_map = json_map
        self.world_map = EmptyMapGenerator(100, 100, self.settings).get_map()

    def _register_decoders(self):
        self.decoders = [
            ScoreCellDecoder("2"),
            ObstacleDecoder("1")
        ]

    def _json_decode_map(self):
        def find_element_by_code(json, code):
            for element in json:
                if element["code"] == str(code):
                    yield element

        for decoder in self.decoders:
            for element in find_element_by_code(self.json_map, decoder.code):
                decoder.decode(element, self.world_map)


class Level1(JsonLevelGenerator):
    def get_map(self):
        self._register_json(LEVELS["level1"])
        self._register_decoders()
        self._json_decode_map()

        return self.world_map
