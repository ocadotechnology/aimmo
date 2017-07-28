from parsers import CellParser
from pprint import pprint

from completion_checks import COMPLETION_CHECKS

__LEVEL_COUNT = 5

class RawLevelGenerator():
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
for lvl in xrange(1, __LEVEL_COUNT + 1):
    lvl_id = "level" + str(lvl)
    LEVELS[lvl_id] = RawLevelGenerator().by_parser(CellParser()).by_map(lvl_id + ".txt").by_models(["objects.json"]).generate_json()

def main():
    pprint(LEVELS["level1"])

if __name__ == '__main__':
    main()
