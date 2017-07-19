import json
from pprint import pprint

class Parser():
    def __init__(self):
        self.__MAPS_FOLDER = "maps"
        self.__MODELS_FOLDER = "models"

    def parse_model(self, model_name):
        with open(self.__MODELS_FOLDER + "/" + model_name) as data_file:
            model = json.load(data_file)
        return model

    def parse_map(self, map_name):
        with open(self.__MAPS_FOLDER + "/" + map_name) as content_file:
            content = content_file.read()
        lines = content.split('\n')
        cells = [list(filter(lambda x: x != '', line.split(" ")))
            for line in lines]
        cells = list(filter(lambda x: x != [], cells))
        return cells


def main():
    parser = Parser()

    model = parser.parse_model("objects.json")
    pprint(model)

    map = parser.parse_map("level1.txt")
    pprint(map)

if __name__ == '__main__':
    main()
