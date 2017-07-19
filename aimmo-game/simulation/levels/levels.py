from simulation.map_generator import *

# We override the older methods
# We need to integrate the new format as we make it -- we might need refactoring in other
# places
class TemplateLevelGenerator(_BaseLevelGenerator):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super(_BaseLevelGenerator, self).__init__(*args, **kwargs)
        self.settings.update(DEFAULT_LEVEL_SETTINGS)

    @abc.abstractmethod
    def get_map(self):
        pass

    @abc.abstractmethod
    def check_complete(self):
        pass
