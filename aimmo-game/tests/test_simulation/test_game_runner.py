from json import dumps

import mock
import pytest
from simulation.avatar.avatar_manager import AvatarManager
from simulation.game_runner import GameRunner
from simulation.game_state import GameState

from .maps import InfiniteMap
from .mock_communicator import MockCommunicator
from .mock_worker_manager import MockWorkerManager


class RequestMock(object):
    def __init__(self, num_users):
        self.value = self._generate_response(num_users)
        self.urls_requested = []

    def _generate_response(self, num_users):
        return {
            "main": {
                "parameters": [],
                "main_avatar": None,
                "users": [
                    {"id": i, "code": "code for %s" % i} for i in range(num_users)
                ],
            }
        }

    def change_code(self, id, new_code):
        users = self.value["main"]["users"]
        for i in range(len(users)):
            if users[i]["id"] == id:
                users[i]["code"] = new_code

    def __call__(self, url, request):
        self.urls_requested.append(url.geturl())
        return dumps(self.value)


@pytest.fixture
def game_runner():
    async def mock_callback():
        pass

    game_state = GameState(InfiniteMap(), AvatarManager())
    game_runner = GameRunner(
        game_state_generator=lambda avatar_manager: game_state,
        port="0000",
        django_api_url="http://test",
        worker_manager_class=MockWorkerManager,
    )

    game_runner.communicator = MockCommunicator()
    game_runner.set_end_turn_callback(mock_callback)
    return game_runner


@pytest.mark.asyncio
async def test_correct_url(game_runner):
    game_runner.communicator.get_game_metadata = mock.MagicMock()
    await game_runner.update()
    # noinspection PyUnresolvedReferences
    game_runner.communicator.get_game_metadata.assert_called_once()


@pytest.mark.asyncio
async def test_workers_and_avatars_added(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    await game_runner.update()

    assert len(game_runner.worker_manager.final_workers) == 3
    for i in range(3):
        assert i in game_runner.game_state.avatar_manager.avatars_by_id
        assert i in game_runner.worker_manager.final_workers
        assert game_runner.worker_manager.get_code(i) == "code for %s" % i


@pytest.mark.asyncio
async def test_changed_code(game_runner):
    game_runner.communicator.data = RequestMock(4).value
    await game_runner.update()
    game_runner.communicator.change_code(0, "changed 0")
    game_runner.communicator.change_code(2, "changed 2")
    await game_runner.update()

    for i in range(4):
        assert i in game_runner.worker_manager.final_workers
        assert i in game_runner.game_state.avatar_manager.avatars_by_id

    for i in (1, 3):
        assert game_runner.worker_manager.get_code(i) in "code for %s" % i

    for i in (0, 2):
        assert i in game_runner.worker_manager.updated_workers
        assert game_runner.worker_manager.get_code(i) in "changed %s" % i


@pytest.mark.asyncio
async def test_logs_cleared_at_each_update(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    await game_runner.update_workers()
    first_worker = game_runner.worker_manager.player_id_to_worker[0]
    first_worker.log = "test logs"

    game_runner.worker_manager.clear_logs()

    assert first_worker.log is None


@pytest.mark.asyncio
async def test_remove_avatars(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    await game_runner.update()
    del game_runner.communicator.data["main"]["users"][1]
    await game_runner.update()

    for i in range(3):
        if i == 1:
            assert i not in game_runner.worker_manager.final_workers
            assert i not in game_runner.game_state.avatar_manager.avatars_by_id
        else:
            assert i in game_runner.worker_manager.final_workers
            assert i in game_runner.game_state.avatar_manager.avatars_by_id


@pytest.mark.asyncio
async def test_turn_increment(game_runner):
    game_runner.communicator.data = RequestMock(3).value
    assert game_runner.game_state.turn_count == 0
    await game_runner.update()
    assert game_runner.game_state.turn_count == 1

