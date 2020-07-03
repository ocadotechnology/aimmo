from unittest import TestCase

import service
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_state import GameState
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location
from simulation.world_map import WorldMap
from .test_simulation.dummy_avatar import MoveEastDummy
from .test_simulation.maps import MockCell, MockPickup
from .test_simulation.mock_game_state import MockGameState


class TestService(TestCase):
    class DummyAvatarManager(AvatarManager):
        avatars = [MoveEastDummy(1, Location(0, -1))]

    @classmethod
    def setUpClass(cls):
        """ Register the api endpoints """
        cls.game_api = service.GameAPI(game_state=MockGameState(None, None))

    def setUp(self):
        """
        Sets up the JSON of the world state generated by the service file for testing.
        """
        self.avatar_manager = self.DummyAvatarManager()

        CELLS = [
            [
                {
                    "interactable": MockPickup("b"),
                    "avatar": self.avatar_manager.avatars[0],
                },
                {},
                {},
            ],
            [{}, {"habitable": False}, {"interactable": MockPickup("a")}],
        ]

        grid = {
            Location(x, y - 1): MockCell(Location(x, y - 1), **CELLS[x][y])
            for y in range(3)
            for x in range(2)
        }
        grid[Location(0, 1)].interactable = ScoreLocation(grid[Location(0, 1)])
        test_game_state = GameState(WorldMap(grid, {}), self.avatar_manager)
        self.world_state_json = test_game_state.serialize()

    def test_correct_json_player_dictionary(self):
        """
        Ensures the "players" element of the get_game_state() JSON returns the correct information for the dummy
        avatar provided into the world.

        NOTE: Orientation (and others) may be hard coded. This test WILL and SHOULD fail if the functionality is added.
        """
        player_list = self.world_state_json["players"]
        self.assertEqual(len(player_list), 1)
        details = player_list[0]
        self.assertEqual(details["id"], 1)
        self.assertEqual(details["location"]["x"], 0)
        self.assertEqual(details["location"]["y"], -1)
        self.assertEqual(details["health"], 5)
        self.assertEqual(details["orientation"], "north")
        self.assertEqual(details["score"], 0)

    def test_correct_json_score_locations(self):
        """
        Ensures the correct score location in the "score_locations" element; is returned by the JSON.
        """
        interactable_list = self.world_state_json["interactables"]
        for interactable in interactable_list:
            if "ScoreLocation" in interactable:
                self.assertEqual(interactable["location"]["x"], 0)
                self.assertEqual(interactable["location"]["y"], 1)

    def test_correct_json_north_east_corner(self):
        """
        Top right corner of the map must be correct to determine the map size.
        """
        north_east_corner = self.world_state_json["northEastCorner"]
        self.assertEqual(north_east_corner["x"], 1)
        self.assertEqual(north_east_corner["y"], 1)

    def test_correct_json_south_west_corner(self):
        """
        Bottom left corner of the map must be correct to determine the map size.
        """
        south_west_corner = self.world_state_json["southWestCorner"]
        self.assertEqual(south_west_corner["x"], 0)
        self.assertEqual(south_west_corner["y"], -1)

    def test_correct_json_era(self):
        """
        Ensure that the era (for the assets in the frontend) is correct.

        NOTE: This is hard coded right now to "future". This test should fail when this functionality is added.
        """
        era = self.world_state_json["era"]
        self.assertEqual(era, "future")

    def test_correct_json_world_interactables_returned_is_correct_amount(self):
        """
        The JSON returns the correct amount of pickups.
        """
        interactable_list = self.world_state_json["interactables"]
        self.assertEqual(len(interactable_list), 3)

    def test_correct_json_world_obstacles(self):
        """
        JSON generated must return correct location, width, height, type and orientation about obstacles.

        NOTE: Obstacles are highly hard coded right now. Only location changes. If any functionality is added, this test
              WILL and SHOULD fail.
        """
        obstacle_list = self.world_state_json["obstacles"]
        self.assertEqual(len(obstacle_list), 1)
        self.assertEqual(obstacle_list[0]["location"]["x"], 1)
        self.assertEqual(obstacle_list[0]["location"]["y"], 0)
        self.assertEqual(obstacle_list[0]["orientation"], "north")
        self.assertEqual(obstacle_list[0]["width"], 1)
        self.assertEqual(obstacle_list[0]["height"], 1)
        self.assertEqual(obstacle_list[0]["type"], "wall")
