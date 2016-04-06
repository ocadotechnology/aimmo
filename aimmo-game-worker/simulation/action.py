from event import *
import world_map as world_map_module


class Action(object):
    def serialise(self):
        raise NotImplementedError


class WaitAction(Action):
    def serialise(self):
        return {
            'action_type': 'wait',
        }


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def serialise(self):
        return {
            'action_type': 'move',
            'options': {
                'direction': self.direction.serialise()
            },
        }


class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def serialise(self):
        return {
            'action_type': 'attack',
            'options': {
                'direction': self.direction.serialise()
            },
        }
