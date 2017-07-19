import json
import abc
from pprint import pprint

from transforms import CellTransform

class Parser():
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.__MAPS_FOLDER = "maps"
        self.__MODELS_FOLDER = "models"
        self.models = []
        self.transforms = {}
        self.map = []

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
        self.map = cells

    def register_model(self, model):
        self.modes.append(parse_model(model))

    def register_models(self, models):
        for model in models:
            self.register_model(model)

    # overwrites transform if present
    def register_transform(self, transform):
        self.transforms[transform.__class__.__name__] = transform

    @abc.abstractmethod
    def register_transforms():
        pass

    def feed_string(self, str):
        # e.g. class:CellTransform.compute_id
        if str.startsWith("class:"):
            model_class = str.split(":")[1].slit(".")[0]
            model_method = str.split(":")[1].slit(".")[0]

            return self.transforms[model_class][model_method]()
        else:
            return str

    def feed_json(self, code):
        def populate(json, model):
            if isinstance(model, list):
                for item in model:
                    json.append(populate({}, item))
                    return json
            elif isinstance(model, string):
                json = self.feed_string(model)
            else:
                for item in model:
                    json[item] = populate(model[item])


        for model_list in models:
            for model in model_list:
                # the model was found
                if model["code"] == code:
                    # populate it and return it
                    json = {}
                    populate(json, model)
                    return json

    def map_apply_transforms(self):
        objects = []
        for x in xrange(len(self.map)):
            for y in xrange(len(self.map[x])):
                code = self.map[x][y]

                self.register_transforms(x, y, code)
                object_json = self.feed_json(code)
                objects.append(object_json)

        return objects

class CellParser(Parser):
    def register_transforms(self, x, y, code):
        self.register_transform(CellTransform(x, y, code))

def main():
    parser = CellParser()
    pprint(parser.map_apply_transforms())

if __name__ == '__main__':
    main()
