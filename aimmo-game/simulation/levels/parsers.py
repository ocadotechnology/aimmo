import json
import abc
from pprint import pprint

from transforms import CellTransform

def call_method(o, name):
    getattr(o, name)()

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
        self.models.append(self.parse_model(model))

    def register_models(self, models):
        for model in models:
            self.register_model(model)

    # overwrites transform if present
    def register_transform(self, transform):
        self.transforms[transform.__class__.__name__] = transform

    @abc.abstractmethod
    def register_transforms():
        pass

    def feed_string(self, input_str):
        if isinstance(input_str, unicode):
            input_str = str(input_str)

        # e.g. class:CellTransform.compute_id
        if input_str.startswith("class:"):
            model_class = input_str.split(":")[1].split(".")[0]
            model_method = input_str.split(":")[1].split(".")[1]

            return call_method(self.transforms[model_class], model_method)
        else:
            return str

    def feed_json(self, code):
        def populate(json, model):
            print("populating json")
            if isinstance(model, list):
                for item in model:
                    json.append(populate({}, item))
                    return json
            elif isinstance(model, basestring):
                json = self.feed_string(model)
            else:
                for item in model:
                    json[item] = populate({}, model[item])

        for model_list in self.models:
            print(model_list)
            for model in model_list:
                # the model was found
                print(model)
                if model["code"] == code:
                    # populate it and return it
                    json = {}
                    populate(json, model)
                    return json
            return None

    def map_apply_transforms(self):
        objects = []
        for x in xrange(len(self.map)):
            for y in xrange(len(self.map[x])):
                code = self.map[x][y]
                print x, y, code

                self.register_transforms(x, y)
                object_json = self.feed_json(code)
                if object_json != None:
                    objects.append(object_json)

        return objects

class CellParser(Parser):
    def register_transforms(self, x, y):
        self.register_transform(CellTransform(x, y))

def main():
    parser = CellParser()
    parser.parse_map("level1.txt")
    parser.register_models(["objects.json"])
    pprint(parser.map_apply_transforms())

if __name__ == '__main__':
    main()
