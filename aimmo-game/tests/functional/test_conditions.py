from unittest import TestCase
from hypothesis import given, assume
from hypothesis import strategies as st
import math
import asyncio

from .mock_world import MockWorld
from simulation.location import Location
from simulation.cell import Cell
from simulation.pickups.pickup_conditions import avatar_on_cell, avatar_on_cell_group, passive


class TestConditions(TestCase):
    def setUp(self):
        self.game = MockWorld()
        self.game.game_state.add_avatar(1, Location(0, 0))

    def test_avatar_on_cell(self):
        cell = self.game.game_state.world_map.get_cell(Location(1, 0))
        condition = avatar_on_cell(cell)
        self.assertFalse(condition(None))

        cell = self.game.game_state.world_map.get_cell(Location(0, 0))
        condition = avatar_on_cell(cell)
        self.assertTrue(condition(None))

    def test_avatar_on_cell_group_when_avatar_not_in_region(self):
        cells = []
        cells.append(self.game.game_state.world_map.get_cell(Location(1, 0)))
        condition = avatar_on_cell_group(cells)
        self.assertFalse(condition(None))

        cells.append(self.game.game_state.world_map.get_cell(Location(1, 1)))
        condition = avatar_on_cell_group(cells)
        self.assertFalse(condition(None))

        cells.append(self.game.game_state.world_map.get_cell(Location(0, 1)))
        condition = avatar_on_cell_group(cells)
        self.assertFalse(condition(None))

    def test_avatar_on_cell_group_when_avatar_in_region(self):
        cells = []
        cells.append(self.game.game_state.world_map.get_cell(Location(0, 0)))
        condition = avatar_on_cell_group(cells)
        self.assertTrue(condition(None))

        cells.append(self.game.game_state.world_map.get_cell(Location(1, 1)))
        condition = avatar_on_cell_group(cells)
        self.assertTrue(condition(None))

        cells.append(self.game.game_state.world_map.get_cell(Location(0, 1)))
        condition = avatar_on_cell_group(cells)
        self.assertTrue(condition(None))

    def test_passive_condition(self):
        condition = passive()
        self.assertTrue(condition(None))
        