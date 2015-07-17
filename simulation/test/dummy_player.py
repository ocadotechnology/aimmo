from simulation.action import MoveAction
from simulation import direction


class DummyPlayer(object):
    def get_next_action(self, world_state, events):
        return MoveAction(direction.EAST)
