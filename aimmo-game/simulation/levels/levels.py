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
        raws = len(self.parser.map)
        cols = len(self.parser.map[0])

        json = self.parser.map_apply_transforms()
        json.append({
            "code": "meta",
            "raws": raws,
            "cols": cols
        })

        return json

LEVELS = {
    "level1" : RawLevelGenerator().by_parser(CellParser()).by_map("level1.txt").by_models(["objects.json"]).generate_json()
}

def main():
    pprint(LEVELS["level1"])

if __name__ == '__main__':
    main()
