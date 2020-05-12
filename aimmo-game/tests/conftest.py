import os

import pytest

from service import setup_application, setup_socketIO_server, GameAPI
from simulation.game_runner import GameRunner
from turn_collector import TurnCollector

from .test_simulation.mock_avatar_manager import MockAvatarManager
from .test_simulation.mock_communicator import MockCommunicator
from .test_simulation.mock_game_state import MockGameState
from .test_simulation.mock_worker_manager import MockWorkerManager


@pytest.fixture
def game_id():
    os.environ["GAME_ID"] = "1"
    yield
    del os.environ["GAME_ID"]


@pytest.fixture
def app():
    return setup_application(should_clean_token=False)


@pytest.fixture
def socketio_server(app):
    return setup_socketIO_server(app, async_handlers=False)


@pytest.fixture
def turn_collector(socketio_server):
    return TurnCollector(socketio_server)


@pytest.fixture
def game_api(app, turn_collector, socketio_server, game_id):
    game_runner = GameRunner(
        game_state_generator=lambda avatar_manager: MockGameState(
            None, MockAvatarManager()
        ),
        communicator=MockCommunicator(),
        port="0000",
        turn_collector=turn_collector,
        worker_manager_class=MockWorkerManager,
    )
    return GameAPI(
        game_state=game_runner.game_state,
        worker_manager=game_runner.worker_manager,
        application=app,
        server=socketio_server,
    )


@pytest.fixture
def client(app, aiohttp_client, loop):
    return loop.run_until_complete(aiohttp_client(app))
