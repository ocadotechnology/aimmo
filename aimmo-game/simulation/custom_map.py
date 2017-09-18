import abc

from simulation.levels.levels import LEVELS

from simulation.location import Location
from simulation.game_state import GameState
from simulation.world_map import WorldMap
from simulation.world_map import world_map_static_spawn_decorator
from simulation.world_map import DEFAULT_LEVEL_SETTINGS

from simulation.pickups import HealthPickup
from simulation.pickups import InvulnerabilityPickup
from simulation.pickups import DamagePickup


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
        world_map = world_map_static_spawn_decorator(world_map, Location(x, y))
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
            for value in json:
                if value["code"] == str(code):
                    yield value

        for decoder in self.decoders:
            for element in find_element_by_code(self.json_map, decoder.code):
                decoder.decode(element, self.world_map)


class Level1(JsonLevelGenerator):
    def get_map(self):
        self._register_json(LEVELS["level1"])
        self._register_decoders()
        self._json_decode_map()

        return self.world_map
