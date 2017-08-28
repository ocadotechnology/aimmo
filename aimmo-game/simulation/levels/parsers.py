import json
import abc
import os
import re

from transforms import CellTransform

def call_method(o, name):
    x = getattr(o, name)()
    return x

class JSONParser():
    """
        A parser that loads a level from a json file.

        We want to keep the old parsers for testing in the back-end, but
        we also want the new formatted maps that are exported from the
        Unity level generator.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, map_name):
        self._SCRIPT_LOCATION = os.path.abspath(os.path.dirname(__file__))
        self._JSON_FOLDER = os.path.join(self._SCRIPT_LOCATION, "json")
        self.map_name = map_name

    def parse_json(self):
        def clean_json(data):
            # cleans trailing json commas
            data = re.sub(",[ \t\r\n]+}", "}", data)
            data = re.sub(",[ \t\r\n]+\]", "]", data)

            return data

        with open(os.path.join(self._JSON_FOLDER, self.map_name), 'r') as data_file:
            data = data_file.read().replace('\n', '')
            self.map = json.loads(clean_json(data))

    def get_objects(self):
        self.parse_json()
        return self.map

class Parser():
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
    def register_transforms():
        pass

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
        for x in xrange(len(self.map)):
            for y in xrange(len(self.map[x])):
                code = self.map[x][y]

                self.register_transforms(x, y)
                object_json = self.feed_json(code)
                if object_json != None:
                    objects.append(object_json)

        return objects

class CellParser(Parser):
    def register_transforms(self, x, y):
        self.register_transform(CellTransform(x, y))
