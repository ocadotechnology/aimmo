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

from simulation.pickups import HealthPickup
from simulation.pickups import InvulnerabilityPickup
from simulation.pickups import DamagePickup

class BaseGenerator(object):
    """
        A map generator that exposes a game state and a check for level completion.

        API:
            - contructor(setting)
                - a set of basic settings that the map uses at generation
                - see DEFAULT_LEVEL_SETTINGS in simulation.world_map
            - get_game_state(avatar_manager)
                - exposes a game state used by the turn manager daemon
                - for details see GameState
            - check_complete(game_state)
                - function to check if a map is "complete"
                - the turn manager runs the action for each avatar, then runs check_complete afterwards
            @abstract
            - get_map
                - returns the generated map

        Important: for the moment level configurations are found directly by their name by looking into
        the module map_generator - look in service.py for:
            generator = getattr(map_generator, settings['GENERATOR'])(settings)
    """
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
    """
        Generates empty maps
        - get_map_by_corners
        - get_map - generates a map with center in (0, 0)
    """
    def __init__(self, settings):
        self.height =  self.settings['START_HEIGHT']
        self.width = self.settings['START_WIDTH']
        self.settings = settings

    def __init__(self, height, width, settings):
        self.height = height
        self.width = width
        self.settings = settings

    @classmethod
    def get_map_by_corners(cls, settings, corners):
        (min_x, max_x, min_y, max_y) = corners
        grid = {}
        for x in xrange(min_x, max_x + 1):
            for y in xrange(min_y, max_y + 1):
                location = Location(x, y)
                grid[location] = Cell(location)
        return WorldMap(grid, settings)

    def get_map(self):
        def get_corners(height, width):
            max_x = int(math.floor(width / 2))
            min_x = -(width - max_x - 1)
            max_y = int(math.floor(height / 2))
            min_y = -(height - max_y - 1)
            return min_x, max_x, min_y, max_y

        new_settings = DEFAULT_LEVEL_SETTINGS.copy()
        new_settings.update(self.settings)

        return EmptyMapGenerator.get_map_by_corners(self.settings, get_corners(self.height, self.width))

class BaseLevelGenerator(BaseGenerator):
    """
        BaseGenerator with default settings.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(BaseLevelGenerator, self).__init__(*args, **kwargs)
        self.settings.update(DEFAULT_LEVEL_SETTINGS)

################################################################################

class Decoder():
    """
        See @JsonLevelGenerator and @Levels first.

        A Decorer is a class that receives a Json formatted as in levels/models
        and decodes it, altering the state of the world_map.

        Decoders are used to translate a Level from the JSON format to the internal
        state of a map(i.e. a WorldMap).

        An example of a JSon format is:
          {
            "code": "1",
            "id" : "5",
            "x" : "3",
            "y" : "3"
          }
    """
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

class PickupDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        if json["type"] == "invulnerability":
            world_map.get_cell(Location(x, y)).pickup = InvulnerabilityPickup(world_map.get_cell(Location(x, y)))
        if json["type"] == "health":
            world_map.get_cell(Location(x, y)).pickup = HealthPickup(world_map.get_cell(Location(x, y)), int(json["health_restored"]))
        if json["type"] == "damage":
            world_map.get_cell(Location(x, y)).pickup = DamagePickup(world_map.get_cell(Location(x, y)))

################################################################################

class JsonLevelGenerator(BaseLevelGenerator):
    """
        Workflow:
            - setup the metadata: map dimensions, etc.
            - register the json that represents the map
            - register the decoders that tranform the jsons into WorldMap objects
            - decode the map applying the decoder to each of the jsons

        All the levels can be found in json format in levels.LEVELS.
        To register a level extend this class.
    """
    def __init__(self, *args, **kwargs):
        super(JsonLevelGenerator, self).__init__(*args, **kwargs)

    def _setup_meta(self):
        # Used so that the map dimension does not increase automatically
        self.settings["TARGET_NUM_CELLS_PER_AVATAR"] = -1000

        # Finds the json with metaiformation
        for element in self.json_map:
            if element["code"] == "meta":
                self.meta = element

        # Sets the empty map to the dimensions of the given level
        self.world_map = EmptyMapGenerator.get_map_by_corners(
            self.settings,
            (0, self.meta["rows"] - 1, 0, self.meta["cols"] - 1))

    def _register_json(self, json_map):
        self.json_map = json_map

    def _register_decoders(self):
        self.decoders = [
            ScoreCellDecoder("2"),
            ObstacleDecoder("1"),
            PickupDecoder("3"),
            PickupDecoder("4"),
            PickupDecoder("5")
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

        self._setup_meta()
        self._register_decoders()
        self._json_decode_map()

        return self.world_map

    def check_complete(self, game_state):
        try:
            main_avatar = game_state.get_main_avatar()
        except KeyError:
            return False

        return main_avatar.score > 24

