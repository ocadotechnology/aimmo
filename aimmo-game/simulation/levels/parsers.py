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

def main():
    parser = Parser()

    model = parser.parse_model("objects.json")
    pprint(model)

if __name__ == '__main__':
    main()
