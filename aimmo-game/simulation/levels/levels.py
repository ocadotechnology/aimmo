from parsers import CellParser, JSONParser
from pprint import pprint

import os

_SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
_MAPS_FOLDER = os.path.join(_SCRIPT_LOCATION, "maps")
_JSON_FOLDER = os.path.join(_SCRIPT_LOCATION, "json")

class RawJSONLevelGenerator():
    """
        Builder that is used for the json levels.

        To add a Unity-generated level:
            -- add a level in the json_folder
    """

    def __init__(self):
        pass

    def by_json_level_name(self, level_name):
        self.parser = JSONParser(level_name)
        return self

    def generate_json(self):
        return self.parser.get_objects()

class RawLevelGenerator():
    """
        Builder that is used to expose json formatted levels.
        See @parsers for details on level generation.

        To see the JSON format of the levels run this file.

        For the moment levels need to be labeled: 1, 2, ... etc.

        To add a new level(locally):
            - add a level*.txt
            - add a completion check
            - modify number of levels in players/app_settings
    """
    def __init__(self):
        pass

    def by_parser(self, parser):
        self.parser = parser
        return self

    def by_map(self, map):
        self.parser.parse_map(map)
        return self

    def by_models(self, models):
        self.parser.register_models(models)
        return self

    def generate_json(self):
        return self.parser.map_apply_transforms()

LEVELS = {}

TXT_LEVELS = os.listdir(_MAPS_FOLDER)
TXT_LEVELS.sort()
for lvl in range(1, len(TXT_LEVELS) + 1):
    lvl_id = "level" + str(lvl)
    LEVELS[lvl_id] = RawLevelGenerator().by_parser(CellParser()).by_map(TXT_LEVELS[lvl - 1]).by_models(["objects.json"]).generate_json()

JSON_LEVELS = os.listdir(_JSON_FOLDER)
JSON_LEVELS.sort()
for lvl in range(len(TXT_LEVELS) + 1, len(JSON_LEVELS) + len(TXT_LEVELS) + 1):
    lvl_id = "level" + str(lvl)
    LEVELS[lvl_id] = RawJSONLevelGenerator().by_json_level_name(JSON_LEVELS[lvl - len(TXT_LEVELS) - 1]).generate_json()

if __name__ == '__main__':
    pprint(LEVELS["level6"])
