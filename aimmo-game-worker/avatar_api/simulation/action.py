from abc import ABCMeta, abstractmethod


class Action:
    __metaclass__ = ABCMeta

    @abstractmethod
    def serialise(self):
        pass


class WaitAction(Action):
    def serialise(self):
        return {"action_type": "wait"}


class PickupAction(Action):
    def serialise(self):
        return {"action_type": "pickup"}


class MoveAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def serialise(self):
        return {
            "action_type": "move",
            "options": {"direction": self.direction.serialise()},
        }


class AttackAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def serialise(self):
        return {
            "action_type": "attack",
            "options": {"direction": self.direction.serialise()},
        }
