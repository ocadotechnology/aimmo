from pprint import pprint
import abc

class BaseSnapshotProcessor():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def receive_snapshot(self, information):
        pass

class SnapshotProcessor(BaseSnapshotProcessor):
    def __init__(self, binder):
        self.binder = binder
        self.world_states = []

    def receive_snapshot(self, world_state_json):
        pprint(world_state_json)
        pass
