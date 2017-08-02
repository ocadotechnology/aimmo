import abc

from simulation.location import Location
from simulation.world_map import WorldMapStaticSpawnDecorator
from simulation.world_map import Cell

from simulation.cell import *

from simulation.pickups import HealthPickup
from simulation.pickups import InvulnerabilityPickup
from simulation.pickups import DamagePickup

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

def get_sprite(json):
    if "sprite" in json:
        return json["sprite"]
    return {}

class ScoreCellDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        world_map = WorldMapStaticSpawnDecorator(world_map, Location(x, y))
        world_map.get_cell(Location(x, y)).cell_content = ScoreLocation(get_sprite(json))

class ObstacleDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        world_map.get_cell(Location(x, y)).cell_content = Obstacle(get_sprite(json))

class PickupDecoder(Decoder):
    def decode(self, json, world_map):
        x, y = int(json["x"]), int(json["y"])
        world_map.get_cell(Location(x, y)).cell_content = Floor(get_sprite(json))
        if json["type"] == "invulnerability":
            world_map.get_cell(Location(x, y)).pickup = InvulnerabilityPickup(world_map.get_cell(Location(x, y)))
        if json["type"] == "health":
            world_map.get_cell(Location(x, y)).pickup = HealthPickup(world_map.get_cell(Location(x, y)), int(json["health_restored"]))
        if json["type"] == "damage":
            world_map.get_cell(Location(x, y)).pickup = DamagePickup(world_map.get_cell(Location(x, y)))

DECODERS = [
    ScoreCellDecoder("2"),
    ObstacleDecoder("1"),
    PickupDecoder("3"),
    PickupDecoder("4"),
    PickupDecoder("5")
]
