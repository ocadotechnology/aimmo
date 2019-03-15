import asyncio
from unittest import TestCase

from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location

from .mock_world import MockWorld


class TestScoreLocationsAndEffects(TestCase):
    def setUp(self):
        """
        Mock a game for each test individually. MockWorld() will set up a:
        avatar manager, game state, turn manager and a map generator.
        """
        self.game = MockWorld()
        self.game.simulation_runner.add_avatar(1, Location(0, 0))
        self.cell = self.game.game_state.world_map.get_cell(Location(0, 0))

        # Avatar will try to move North, so we force it to stay in place
        self.game.game_state.world_map.get_cell(
            Location(1, 0)).habitable = False

    def test_score_location_increase_score_of_avatar(self):
        """
        Avatar spawns at the origin (0,0) and should have a score of 0. Moves
        EAST to (1,0) and should automatically then receive an effect that will
        increase the avatars score.
        """
        self.cell.interactable = ScoreLocation(self.cell)
        self.assertEqual(self.game.avatar_manager.get_avatar(1).score, 0)
        self.assertEqual(self.cell.interactable.serialize(), {
            'type': 'score',
            'location': {
                'x': self.cell.location.x,
                'y': self.cell.location.y,
            }
        })

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialized_action()))

        self.assertEqual(self.cell.avatar,
                         self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.score, 1)
        self.assertEqual(len(self.cell.avatar.effects), 1)

    def test_score_locations_persist_and_keep_giving_score_effects(self):
        """
        Checks if score can be increased more than once. First moved from ORIGIN to 1,0 ->
        then picks up the pickup, and moves to 2,0 to do the same.
        """
        loop = asyncio.get_event_loop()
        self.cell.interactable = ScoreLocation(self.cell)
        loop.run_until_complete(self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialized_action()))
        self.assertEqual(self.cell.avatar,
                         self.game.avatar_manager.get_avatar(1))
        self.assertEqual(self.cell.avatar.score, 1)

        loop.run_until_complete(self.game.simulation_runner.run_single_turn(
            self.game.avatar_manager.get_player_id_to_serialized_action()))

        self.assertEqual(self.cell.avatar.score, 2)
        self.assertEqual(self.cell.avatar,
                         self.game.avatar_manager.get_avatar(1))
