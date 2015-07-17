dummy = '''from simulation.action import MoveAction
from simulation import direction


class Avatar(object):
    def handle_turn(self, world_state, events):
        return MoveAction(direction.EAST)
'''