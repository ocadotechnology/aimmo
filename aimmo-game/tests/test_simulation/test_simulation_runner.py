from __future__ import absolute_import

from string import ascii_uppercase
from unittest.mock import patch, Mock

from simulation.avatar.avatar_appearance import AvatarAppearance
from simulation.game_logic import PickupUpdater
from simulation.worksheet.worksheet import WorksheetData
from simulation.interactables.pickups import YellowOrbArtefact
from simulation.interactables.score_location import ScoreLocation
from simulation.location import Location
from simulation.simulation_runner import ConcurrentSimulationRunner
from simulation.world_map import WorldMap
from turn_collector import CollectedTurnActions

from .dummy_avatar import (
    DeadDummy,
    DummyAvatar,
    DummyAvatarManager,
    MoveEastDummy,
    MoveNorthDummy,
    MoveSouthDummy,
    MoveWestDummy,
    WaitDummy,
)
from .maps import InfiniteMap, MockCell, MockPickup
from .mock_communicator import MockCommunicator
from .mock_game_state import MockGameState

ORIGIN = Location(0, 0)

RIGHT_OF_ORIGIN = Location(1, 0)
FIVE_RIGHT_OF_ORIGIN = Location(5, 0)

ABOVE_ORIGIN = Location(0, 1)
FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE = Location(5, 1)

SETTINGS = {
    "TARGET_NUM_CELLS_PER_AVATAR": 0,
    "TARGET_NUM_PICKUPS_PER_AVATAR": 0,
    "TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR": 0,
    "SCORE_DESPAWN_CHANCE": 0,
    "PICKUP_SPAWN_CHANCE": 0,
}


def generate_grid(columns=2, rows=2):
    alphabet = iter(ascii_uppercase)
    grid = {
        Location(x, y): MockCell(Location(x, y), name=next(alphabet))
        for x in range(columns)
        for y in range(rows)
    }
    return grid


class TestSimulationRunner:
    """
    Key:
        > : Avatar moving eastward
        < : Avatar moving westward
        x : Avatar waiting / blocked
        o : Avatar successfully moved
        ! : Dead avatar (that should be waiting)
    """

    def assertGridSize(self, world_map, expected_columns, expected_rows=None):
        if expected_rows is None:
            expected_rows = expected_columns
        assert world_map.num_rows == expected_rows
        assert world_map.num_cols == expected_columns
        assert world_map.num_cells == expected_rows * expected_columns
        assert len(list(world_map.all_cells())) == expected_rows * expected_columns

    def construct_default_avatar_appearance(self):
        return AvatarAppearance("#000", "#ddd", "#777", "#fff")

    def construct_simulation_runner(self, avatars, locations):
        self.avatar_manager = DummyAvatarManager(avatars)
        self.avatar_manager.avatars_by_id = dict(enumerate(avatars))
        self.game_state = MockGameState(InfiniteMap(), self.avatar_manager)
        self.simulation_runner = ConcurrentSimulationRunner(
            game_state=self.game_state, communicator=MockCommunicator()
        )
        for index, location in enumerate(locations):
            self.simulation_runner.add_avatar(index, location)

    def assert_at(self, avatar, location):
        assert avatar.location == location
        cell = self.game_state.world_map.get_cell(location)
        assert cell.avatar == avatar

    def get_avatar(self, player_id):
        return self.avatar_manager.get_avatar(player_id)

    async def run_turn(self):
        await self.simulation_runner.run_turn(CollectedTurnActions(0))

    def test_add_avatar(self):
        self.construct_simulation_runner([], [])

        self.simulation_runner.add_avatar(7)
        assert 7 in self.game_state.avatar_manager.avatars_by_id

    def test_remove_avatar(self):
        self.construct_simulation_runner(
            [DummyAvatar, DummyAvatar], [Location(0, 0), Location(1, 1)]
        )

        avatar = self.get_avatar(1)
        avatar.marked = True

        self.simulation_runner.remove_avatar(0)

        assert not 0 in self.avatar_manager.avatars_by_id
        assert self.game_state.world_map.get_cell(Location(0, 0)).avatar == None

        assert self.avatar_manager.avatars_by_id[1].marked
        assert self.game_state.world_map.get_cell(Location(1, 1)).avatar.marked

    def test_remove_non_existent_avatar(self):
        self.construct_simulation_runner([], [])
        self.simulation_runner.remove_avatar(10)

    def test_updates_map_with_correct_num_avatars(self):
        self.construct_simulation_runner([], [])

        self.avatar_manager.add_avatar(1)
        self.simulation_runner.update_environment()
        assert len(self.simulation_runner.game_state.avatar_manager.avatars_by_id) == 1

        self.avatar_manager.add_avatar(2)
        self.avatar_manager.add_avatar(3)
        self.simulation_runner.update_environment()
        assert len(self.simulation_runner.game_state.avatar_manager.avatars_by_id) == 3

    def test_grid_does_not_expand(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_CELLS_PER_AVATAR"] = 4
        self.simulation_runner.game_state.world_map = WorldMap(
            generate_grid(), settings
        )
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        self.assertGridSize(self.simulation_runner.game_state.world_map, 2)

    def test_score_despawn_chance(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR"] = 0
        grid = generate_grid()
        grid[Location(0, 1)].interactable = ScoreLocation(grid[Location(0, 1)])
        self.simulation_runner.game_state.world_map = WorldMap(grid, settings)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert (
            grid[Location(0, 1)]
            in self.simulation_runner.game_state.world_map.score_cells()
        )
        assert len(list(self.simulation_runner.game_state.world_map.score_cells())) == 1

    def test_scores_applied(self):
        self.construct_simulation_runner([], [])
        grid = generate_grid()
        avatar = DummyAvatar()
        grid[Location(1, 1)].interactable = ScoreLocation(grid[Location(1, 1)])
        grid[Location(1, 1)].avatar = avatar
        self.simulation_runner.game_state.world_map = WorldMap(grid, SETTINGS)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert avatar.score == 1

    def test_scores_not_added_when_at_target(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR"] = 1
        grid = generate_grid()
        grid[Location(0, 1)].interactable = ScoreLocation(grid[Location(0, 1)])
        self.simulation_runner.game_state.world_map = WorldMap(grid, settings)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert len(list(self.simulation_runner.game_state.world_map.score_cells())) == 1
        assert (
            grid[Location(0, 1)]
            in self.simulation_runner.game_state.world_map.score_cells()
        )

    def test_not_enough_score_space(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_SCORE_LOCATIONS_PER_AVATAR"] = 1
        grid = generate_grid(1, 1)
        grid[Location(0, 0)].avatar = "avatar"
        self.simulation_runner.game_state.world_map = WorldMap(grid, settings)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert len(list(self.simulation_runner.game_state.world_map.score_cells())) == 0

    def test_pickups_added(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_PICKUPS_PER_AVATAR"] = 1
        settings["PICKUP_SPAWN_CHANCE"] = 1
        self.simulation_runner.game_state.world_map = WorldMap(
            generate_grid(), settings
        )
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert (
            len(list(self.simulation_runner.game_state.world_map.interactable_cells()))
            == 1
        )

        self.simulation_runner.update(2, self.simulation_runner.game_state)
        assert (
            len(list(self.simulation_runner.game_state.world_map.interactable_cells()))
            == 2
        )

    def test_pickups_applied(self):
        self.construct_simulation_runner([], [])
        grid = generate_grid()
        avatar = DummyAvatar()
        pickup = MockPickup(target=avatar)
        grid[Location(1, 1)].interactable = pickup
        grid[Location(1, 1)].avatar = avatar
        self.simulation_runner.game_state.world_map = WorldMap(grid, SETTINGS)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert pickup.applied_to == avatar

    def test_pickups_not_added_when_at_target(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_PICKUPS_PER_AVATAR"] = 1
        grid = generate_grid()
        grid[Location(0, 1)].interactable = YellowOrbArtefact(grid[Location(0, 1)])
        self.simulation_runner.game_state.world_map = WorldMap(grid, settings)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert (
            len(list(self.simulation_runner.game_state.world_map.interactable_cells()))
            == 1
        )
        assert (
            grid[Location(0, 1)]
            in self.simulation_runner.game_state.world_map.interactable_cells()
        )

    def test_not_enough_pickup_space(self):
        self.construct_simulation_runner([], [])
        settings = SETTINGS.copy()
        settings["TARGET_NUM_PICKUPS_PER_AVATAR"] = 1
        grid = generate_grid(1, 1)
        grid[Location(0, 0)].interactable = ScoreLocation(grid[Location(0, 0)])
        self.simulation_runner.game_state.world_map = WorldMap(grid, settings)
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        assert (
            len(list(self.simulation_runner.game_state.world_map.pickup_cells())) == 0
        )

    def test_updates_map_based_on_worksheet(self):
        self.construct_simulation_runner([], [])
        map_updater: Mock = Mock(wraps=PickupUpdater)
        worksheet_with_mock_updater = WorksheetData(
            worksheet_id=1,
            era="test era",
            number_of_obstacle_textures=1,
            map_updaters=[map_updater(pickup_types=[YellowOrbArtefact])],
        )
        self.simulation_runner.worksheet = worksheet_with_mock_updater
        self.simulation_runner.update(1, self.simulation_runner.game_state)
        map_updater.assert_called_once()

    async def test_run_turn(self, loop):
        """
        Given:  > _
        (1)
        Expect: _ o
        """
        self.construct_simulation_runner([MoveEastDummy], [ORIGIN])
        avatar = self.get_avatar(0)

        self.assert_at(avatar, ORIGIN)
        await self.run_turn()
        self.assert_at(avatar, RIGHT_OF_ORIGIN)

    async def test_run_several_turns(self, loop):
        """
        Given:  > _ _ _ _ _
        (5)
        Expect: _ _ _ _ _ o
        """
        self.construct_simulation_runner([MoveEastDummy], [ORIGIN])
        avatar = self.get_avatar(0)

        assert avatar.location == ORIGIN
        [await self.run_turn() for _ in range(5)]
        assert avatar.location == FIVE_RIGHT_OF_ORIGIN

    async def test_run_several_turns_and_avatars(self, loop):
        """
        Given:  > _ _ _ _ _
                > _ _ _ _ _
        (5)
        Expect: _ _ _ _ _ o
                _ _ _ _ _ o
        """
        self.construct_simulation_runner(
            [MoveEastDummy, MoveEastDummy], [ORIGIN, ABOVE_ORIGIN]
        )
        avatar0 = self.get_avatar(0)
        avatar1 = self.get_avatar(1)

        self.assert_at(avatar0, ORIGIN)
        self.assert_at(avatar1, ABOVE_ORIGIN)
        [await self.run_turn() for _ in range(5)]
        self.assert_at(avatar0, FIVE_RIGHT_OF_ORIGIN)
        self.assert_at(avatar1, FIVE_RIGHT_OF_ORIGIN_AND_ONE_ABOVE)

    async def test_move_chain_succeeds(self, loop):
        """
        Given:  > > > > > _

        Expect: _ o o o o o
        """
        self.construct_simulation_runner(
            [MoveEastDummy for _ in range(5)], [Location(x, 0) for x in range(5)]
        )
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(5)]
        await self.run_turn()
        [self.assert_at(avatars[x], Location(x + 1, 0)) for x in range(5)]

    async def test_move_chain_fails_occupied(self, loop):
        """
        Given:  > > x _

        Expect: x x x _
        """
        self.construct_simulation_runner(
            [MoveEastDummy, MoveEastDummy, WaitDummy],
            [Location(x, 0) for x in range(3)],
        )
        avatars = [self.get_avatar(i) for i in range(3)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]
        await self.run_turn()
        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]

    async def test_move_chain_fails_occupied_by_dead_avatar(self, loop):
        """
        Given: > > ! _

        Expect: x x ! _
        """

        self.construct_simulation_runner(
            [MoveEastDummy, MoveEastDummy, DeadDummy],
            [Location(x, 0) for x in range(3)],
        )
        avatars = [self.get_avatar(i) for i in range(3)]

        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]
        await self.run_turn()
        [self.assert_at(avatars[x], Location(x, 0)) for x in range(3)]

    async def test_move_fails_collision(self, loop):
        """
        Given: > _ <
        Expect: x _ x
        """

        self.construct_simulation_runner(
            [MoveEastDummy, MoveWestDummy], [Location(0, 0), Location(2, 0)]
        )
        avatars = [self.get_avatar(i) for i in range(2)]

        self.assert_at(avatars[0], Location(0, 0))
        self.assert_at(avatars[1], Location(2, 0))

        await self.run_turn()

        self.assert_at(avatars[0], Location(0, 0))
        self.assert_at(avatars[1], Location(2, 0))

    async def test_move_chain_fails_collision(self, loop):
        """
        Given:  > > > _ <
        (1)
        Expect: x x x _ x
        """
        locations = [Location(0, 0), Location(1, 0), Location(2, 0), Location(4, 0)]
        self.construct_simulation_runner(
            [MoveEastDummy, MoveEastDummy, MoveEastDummy, MoveWestDummy], locations
        )
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        await self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(4)]

    async def test_move_chain_fails_cycle(self, loop):
        """
        Given:  > v
                ^ <
        (1)
        Expect: x x
                x x
        """
        locations = [Location(0, 1), Location(1, 1), Location(1, 0), Location(0, 0)]
        self.construct_simulation_runner(
            [MoveEastDummy, MoveSouthDummy, MoveWestDummy, MoveNorthDummy], locations
        )
        avatars = [self.get_avatar(i) for i in range(4)]

        [self.assert_at(avatars[i], locations[i]) for i in range(4)]
        await self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(4)]

    async def test_move_chain_fails_spiral(self, loop):
        """
        Given:  > > v
                  ^ <
        (1)
        Expect: x x x
                  x x
        """
        locations = [
            Location(0, 1),
            Location(1, 1),
            Location(2, 1),
            Location(2, 0),
            Location(1, 0),
        ]
        self.construct_simulation_runner(
            [
                MoveEastDummy,
                MoveEastDummy,
                MoveSouthDummy,
                MoveWestDummy,
                MoveNorthDummy,
            ],
            locations,
        )
        avatars = [self.get_avatar(i) for i in range(5)]

        [self.assert_at(avatars[i], locations[i]) for i in range(5)]
        await self.run_turn()
        [self.assert_at(avatars[i], locations[i]) for i in range(5)]
