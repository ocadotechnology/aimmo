from parsers import CellParser
from pprint import pprint

import os

_SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
_MAPS_FOLDER = os.path.join(_SCRIPT_LOCATION, "maps")
_LEVEL_COUNT = len(os.listdir(_MAPS_FOLDER))

class RawLevelGenerator():
<<<<<<< HEAD
=======
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
>>>>>>> 9c345e3... Documented level addition workflow.
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
for lvl in xrange(1, _LEVEL_COUNT + 1):
    lvl_id = "level" + str(lvl)
    LEVELS[lvl_id] = RawLevelGenerator().by_parser(CellParser()).by_map(lvl_id + ".txt").by_models(["objects.json"]).generate_json()

def main():
    pprint(LEVELS["level1"])

if __name__ == '__main__':
    main()
