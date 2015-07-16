import unittest

from simulation.location import Location
from simulation.player_manager import PlayerManager
from simulation.turn_manager import TurnManager
from simulation.world_map import WorldMap
from simulation.world_state import WorldState
from simulation.test.dummy_player import DummyPlayer


class TestTurnManager(unittest.TestCase):
    def construct_turn_manager(self, *players):
        self.player_manager = PlayerManager(players)
        self.world_state = WorldState(WorldMap(), self.player_manager)
        self.turn_manager = TurnManager(self.world_state, self.player_manager)

    def test_run_turn(self):
        player = DummyPlayer(Location(0, 0))
        self.construct_turn_manager(player)
        self.turn_manager.run_turn()
        self.assertEqual(player.location, Location(1, 0))

    def test_run_several_turns(self):
        player = DummyPlayer(Location(0, 0))
        self.construct_turn_manager(player)
        [self.turn_manager.run_turn() for _ in xrange(5)]
        self.assertEqual(player.location, Location(5, 0))

    def test_run_several_turns_and_players(self):
        player1 = DummyPlayer(Location(0, 0))
        player2 = DummyPlayer(Location(0, 1))
        self.construct_turn_manager(player1, player2)
        [self.turn_manager.run_turn() for _ in xrange(5)]
        self.assertEqual(player1.location, Location(5, 0))
        self.assertEqual(player2.location, Location(5, 1))

if __name__ == '__main__':
    unittest.main()
