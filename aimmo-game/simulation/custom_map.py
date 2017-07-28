import abc

from simulation.levels.levels import LEVELS

from simulation.location import Location
from simulation.game_state import GameState
from simulation.world_map import WorldMap
from simulation.world_map import WorldMapStaticSpawnDecorator
from simulation.world_map import DEFAULT_LEVEL_SETTINGS
from simulation.world_map import Cell

from simulation.pickups import HealthPickup
from simulation.pickups import InvulnerabilityPickup
from simulation.pickups import DamagePickup

import sys
current_module = sys.modules[__name__]

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

class PickupDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        if json["type"] == "invulnerability":
            world_map.get_cell(Location(x, y)).pickup = InvulnerabilityPickup(Location(x, y))
        if json["type"] == "health":
            world_map.get_cell(Location(x, y)).pickup = HealthPickup(Location(x, y), int(json["health_restored"]))
        if json["type"] == "damage":
            world_map.get_cell(Location(x, y)).pickup = DamagePickup(Location(x, y))

################################################################################

class JsonLevelGenerator(TemplateLevelGenerator):
    def _register_json(self, json_map):
        self.json_map = json_map
        self.world_map = WorldMap.generate_empty_map(15, 15, self.settings)

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

#### Dragons be here

def check_complete(self, game_state):
    try:
        main_avatar = game_state.get_main_avatar()
    except KeyError:
        return False

    return main_avatar.score > 24

def generate_level_class(level_nbr, check_complete):
    level_name = "Level" + str(level_nbr)

    def get_map_by_level(level_nbr):
        def get_map(self):
            self._register_json(LEVELS["level" + str(level_nbr)])

            self._setup_meta()
            self._register_decoders()
            self._json_decode_map()

            return self.world_map

        return get_map

    ret_class = type(level_name, (JsonLevelGenerator,), {
        "get_map": get_map_by_level(level_nbr),
        "check_complete": check_complete
    })

    return ret_class

for cur_level in xrange(1, len(LEVELS) + 1):
    gen_class = generate_level_class(cur_level, check_complete)
    setattr(current_module, gen_class.__name__, gen_class)
