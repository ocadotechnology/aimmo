from unittest import TestCase

from simulation.cell import Cell
from .test_world_map import serializer


class TestCell(TestCase):
    def test_equal(self):
        cell1 = Cell(1)
        cell2 = Cell(1)
        self.assertEqual(cell1, cell2)

    def test_not_equal(self):
        cell1 = Cell(1)
        cell2 = Cell(2)
        self.assertNotEqual(cell1, cell2)

    def _create_full_cell(self):
        cell = Cell(serializer('location'), False, True)
        cell.avatar = serializer('avatar')
        cell.interactable = serializer('pickup')
        self.expected = {
            'avatar': 'avatar',
            'generates_score': True,
            'habitable': False,
            'location': 'location',
            'pickup': 'pickup',
            'partially_fogged': False
        }
        return cell

    def test_serialize(self):
        cell = self._create_full_cell()
        self.assertEqual(cell.serialize(), self.expected)

    def test_serialize_no_avatar(self):
        cell = self._create_full_cell()
        cell.avatar = None
        self.expected['avatar'] = None
        self.assertEqual(cell.serialize(), self.expected)

    def test_serialize_no_pickup(self):
        cell = self._create_full_cell()
        cell.interactable = None
        self.expected['pickup'] = None
        self.assertEqual(cell.serialize(), self.expected)
