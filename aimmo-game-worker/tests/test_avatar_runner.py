from unittest import TestCase
from avatar_runner import AvatarRunner

NORTH = {'x': 0, 'y': 1}
SOUTH = {'x': 0, 'y': -1}
EAST = {'x': 1, 'y': 0}
WEST = {'x': -1, 'y': 0}


class TestAvatarRunner(TestCase):
    def test_runner_does_not_crash_on_code_errors(self):
        class Avatar(object):
            def handle_turn(self, world_map, avatar_state):
                assert False

        runner = AvatarRunner(avatar=Avatar(), auto_update=False)
        action = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code='')['action']
        self.assertEqual(action, {'action_type': 'wait'})

    def test_runner_updates_code_on_change(self):
        avatar1 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import EAST
                            
                            return MoveAction(EAST)
                  '''
        avatar2 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import WEST
                            
                            return MoveAction(WEST)
                  '''

        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': EAST}})

        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)

        self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': WEST}})

    def test_runner_can_maintain_state(self):
        """ This test ensures that if the code is the same, we do not recreate the avatar object in the runner.
            We check this by making sure that self.x is being updated and its value retained. """

        avatar = '''class Avatar(object):
                        def __init__(self):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH, SOUTH, EAST, WEST
                            
                            self.moves = [MoveAction(NORTH), MoveAction(EAST), MoveAction(SOUTH), MoveAction(WEST)]
                            self.x = 0
                            
                        def handle_turn(self, world_map, avatar_state):
                            move = self.moves[self.x]
                            self.x += 1
                            return move
                 '''
        runner = AvatarRunner()

        directions = [NORTH, EAST, SOUTH, WEST]
        for direction in directions:
            response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar)
            self.assertEqual(response['action'], {'action_type': 'move', 'options': {'direction': direction}})

    def test_update_code_flag(self):
        avatar1 = '''class Avatar(object):
                        def handle_turn(self, world_map, avatar_state):
                            from simulation.action import MoveAction
                            from simulation.direction import NORTH
                            
                            return MoveAction(NORTH)
                  '''
        avatar2 = '''class Avatar(object):
                                def handle_turn(self, world_map, avatar_state):
                                    from simulation.action import MoveAction
                                    from simulation.direction import SOUTH

                                    return MoveAction(SOUTH)
                  '''

        runner = AvatarRunner()
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertTrue(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar1)
        self.assertFalse(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)
        self.assertTrue(response['avatar_updated'])
        response = runner.process_avatar_turn(world_map={}, avatar_state={}, src_code=avatar2)
        self.assertFalse(response['avatar_updated'])
