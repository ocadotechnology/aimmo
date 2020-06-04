from json import dumps

import pytest

import mock
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_runner import GameRunner
from simulation.game_state import GameState

from .maps import InfiniteMap
from .mock_communicator import MockCommunicator


class RequestMock(object):
    def __init__(self, num_users):
        self.value = self._generate_response(num_users)
        self.urls_requested = []

    def _generate_response(self, num_users):
        return {
            "main_avatar": None,
            "users": [{"id": i, "code": "code for %s" % i} for i in range(num_users)],
        }

    def change_code(self, id, new_code):
        users = self.value["users"]
        for i in range(len(users)):
            if users[i]["id"] == id:
                users[i]["code"] = new_code

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)


@pytest.fixture
def game_runner(turn_collector):
    async def mock_callback():
        pass

    game_state = GameState(InfiniteMap(), AvatarManager())
    game_runner = GameRunner(
        game_state_generator=lambda avatar_manager: game_state,
        port="0000",
        communicator=MockCommunicator(),
        turn_collector=turn_collector,
    )

    game_runner.set_end_turn_callback(mock_callback)
    return game_runner


@pytest.mark.asyncio
async def test_correct_url(game_runner):
    game_runner.communicator.get_game_metadata = mock.MagicMock()
    await game_runner.update()
    # noinspection PyUnresolvedReferences
    game_runner.communicator.get_game_metadata.assert_called_once()


@pytest.mark.asyncio
async def test_avatars_added(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    await game_runner.update()

    for i in range(3):
        assert i in game_runner.game_state.avatar_manager.avatars_by_id


@pytest.mark.asyncio
async def test_avatar_logs_cleared_at_each_update(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    await game_runner.update_avatars()
    first_avatar = game_runner.game_state.avatar_manager.avatars_by_id[0]
    first_avatar.logs.append("avatar test logs")

    await game_runner.update()

    assert first_avatar.logs == []


@pytest.mark.asyncio
async def test_remove_avatars(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    await game_runner.update()
    del game_runner.communicator.data["users"][1]
    await game_runner.update()

    for i in range(3):
        if i == 1:
            assert i not in game_runner.game_state.avatar_manager.avatars_by_id
        else:
            assert i in game_runner.game_state.avatar_manager.avatars_by_id


@pytest.mark.asyncio
async def test_turn_increment(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    assert game_runner.game_state.turn_count == 0
    await game_runner.update()
    assert game_runner.game_state.turn_count == 1
