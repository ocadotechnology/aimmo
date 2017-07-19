from parsers import CellParser
from pprint import pprint

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

LEVELS = {
    "level1" : RawLevelGenerator().by_parser(CellParser()).by_map("level1.txt").by_models(["objects.json"]).generate_json()
}

def main():
    pprint(LEVELS["level1"])

if __name__ == '__main__':
    main()
