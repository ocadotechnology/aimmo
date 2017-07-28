from parsers import CellParser
from pprint import pprint

__LEVEL_COUNT = 5

class RawLevelGenerator():
    """
        Builder that is used to expose json formatted levels.
        See @parsers for details on level generation.

        To see the JSON format of the levels run this file.
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
        rows = len(self.parser.map)
        cols = len(self.parser.map[0])

        json = self.parser.map_apply_transforms()
        json.append({
            "code": "meta",
            "rows": rows,
            "cols": cols
        })

        return json

LEVELS = {}
for lvl in xrange(1, __LEVEL_COUNT + 1):
    LEVELS["level" + str(lvl)] = RawLevelGenerator().by_parser(CellParser()).by_map("level" + str(lvl) + ".txt").by_models(["objects.json"]).generate_json()

def main():
    pprint(LEVELS["level1"])

if __name__ == '__main__':
    main()
