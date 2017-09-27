from __future__ import absolute_import

from unittest import TestCase

from simulation.avatar.fog_of_war import should_partially_fog, partially_fog_cell
from simulation.maps.cell import Cell

class Serialiser(object):
    def __init__(self, content):
        self.content = content

    def serialise(self):
        return self.content


class TestFogOfWar(TestCase):
    def test_should_partially_fog(self):
        self.assertFalse(should_partially_fog(no_fog_distance=20, partial_fog_distance=2, x_dist=1, y_dist=10))
        self.assertTrue(should_partially_fog(no_fog_distance=1, partial_fog_distance=2, x_dist=20, y_dist=10))

    def _create_full_cell(self):
        cell = Cell(Serialiser('location'), False, True)
        cell.avatar = Serialiser('avatar')
        cell.pickup = Serialiser('pickup')
        self.expected = {
            'avatar': 'avatar',
            'generates_score': True,
            'habitable': False,
            'location': 'location',
            'pickup': 'pickup',
            'partially_fogged': False
        }
        return cell

    def test_partially_fog_cell(self):
        mock_cell = self._create_full_cell()
        self.assertEqual(mock_cell.partially_fogged, False)
        self.assertEqual(mock_cell.habitable, False)
        self.assertNotEqual(mock_cell.avatar, None)
        self.assertEqual(mock_cell.generates_score, True)
        self.assertNotEqual(mock_cell.pickup, None)

        mock_cell = partially_fog_cell(mock_cell)
        self.assertEqual(mock_cell.partially_fogged, True)
        self.assertEqual(mock_cell.habitable, True)
        self.assertEqual(mock_cell.avatar, None)
        self.assertEqual(mock_cell.pickup, None)
