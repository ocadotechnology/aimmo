from __future__ import absolute_import
from unittest import TestCase

from simulation.action import WaitAction, MoveAction, AttackAction
from simulation.direction import NORTH


class TestAction(TestCase):
    def test_wait_action(self):
        wait_action = WaitAction()

        self.assertEqual(wait_action.serialise()['action_type'], 'wait')

    def test_move_action(self):
        move_action = MoveAction(NORTH)
        self.assertEqual(move_action.direction.x, 0)
        self.assertEqual(move_action.direction.y, 1)

        self.assertEqual(move_action.serialise()['action_type'], 'move')
        self.assertEqual(move_action.serialise()['options']['direction'],
                         NORTH.serialise())

    def test_attack_action(self):
        attack_action = AttackAction(NORTH)
        self.assertEqual(attack_action.direction.x, 0)
        self.assertEqual(attack_action.direction.y, 1)

        self.assertEqual(attack_action.serialise()['action_type'], 'attack')
        self.assertEqual(attack_action.serialise()['options']['direction'],
                         NORTH.serialise())
