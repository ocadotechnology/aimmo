import json
import abc
import os

from pprint import pprint

from transforms import CellTransform

def call_method(o, name):
    x = getattr(o, name)()
    return x

class Parser():
    """
    The parser gets a level formatted as a 2D grid from numbers and transforms each number
    into a json representing that particular object.

    A *map* is a *.txt file composed out of numbers. Each numbers represent a cell in the
    grid that will be eventually generated.

    A *model* is an array of jsons. Each json has an associated code. By that associated code,
    the numbers in the *map* get translated into an json. To see how the final exported version
    of a map looks like, run levels.py.

    A *transform* is an instance of a class that can be called inside a model. A function can be
    called by prepending "class:" before the class name and function name.
    (e.g. class:CellTransform.get_x)

    API:
    - parse_model
        - gets the model name as a string and parsers the model from the folder models
    - parse_map:
        - changes the parser's associated map with map at the given path
    - register model/s
        - adds a new model to the model list
    - register transform
        - register an instance of a transform, so it can be used from *.json file

    - map_apply_transfroms
        - transforms a map formated as a list of numbers into a map formatted as list of jsons

    @abstract
    - register_transforms
        - register all transforms that can be used by the parser

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
        self._MAPS_FOLDER = os.path.join(self._SCRIPT_LOCATION, "maps")
        self._MODELS_FOLDER = os.path.join(self._SCRIPT_LOCATION, "models")
        self.models = []
        self.transforms = {}
        self.map = []

    def parse_model(self, model_name):
        with open(os.path.join(self._MODELS_FOLDER, model_name)) as data_file:
            model = json.load(data_file)
        return model

    def parse_map(self, map_name):
        with open(os.path.join(self._MAPS_FOLDER, map_name)) as content_file:
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
    def register_transforms(self, x, y, width, height):
        pass

    # helper function for map_apply_transforms
    def feed_string(self, input_str):
        if isinstance(input_str, unicode):
            input_str = str(input_str)

        # e.g. class:CellTransform.compute_id
        if input_str.startswith("class:"):
            model_class = input_str.split(":")[1].split(".")[0]
            model_method = input_str.split(":")[1].split(".")[1]

            out = call_method(self.transforms[model_class], model_method)
            return str(out)
        else:
            return input_str

    # helper function for map_apply_transforms
    def feed_json(self, code):
        def populate(json, model):
            if isinstance(model, list):
                for item in model:
                    json.append(populate({}, item))
            elif isinstance(model, basestring):
                json = self.feed_string(model)
            else:
                for item in model:
                    json[item] = populate({}, model[item])
            return json

        for model_list in self.models:
            for model in model_list:
                if model["code"] == code:
                    return populate({}, model)
        return None

    def map_apply_transforms(self):
        objects = []
        width = len(self.map)
        height = len(self.map[0])
        for x in xrange(width):
            for y in xrange(height):
                code = self.map[x][y]

                self.register_transforms(x, y, width, height)
                object_json = self.feed_json(code)
                if object_json != None:
                    objects.append(object_json)

        return objects

class CellParser(Parser):
    def register_transforms(self, x, y, width, height):
        self.register_transform(CellTransform(x, y, width, height))
