import os

import pytest
from activity_monitor import ActivityMonitor
from aioresponses import aioresponses
from mock import MagicMock
from service import GameAPI, setup_application, setup_socketIO_server
from simulation.game_runner import GameRunner
from turn_collector import TurnCollector

from .test_simulation.mock_avatar_manager import MockAvatarManager
from .test_simulation.mock_communicator import MockCommunicator
from .test_simulation.mock_game_state import MockGameState


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mocked:
        yield mocked


@pytest.fixture
def game_id():
    os.environ["GAME_ID"] = "1"
    yield
    del os.environ["GAME_ID"]


@pytest.fixture
def app():
    return setup_application(MockCommunicator(), should_clean_token=False)


@pytest.fixture
def socketio_server(app):
    return setup_socketIO_server(app)


@pytest.fixture
def turn_collector(socketio_server):
    return TurnCollector(socketio_server)


@pytest.fixture
def game_api(app, turn_collector, socketio_server, game_id):
    communicator = MockCommunicator()
    game_runner = GameRunner(
        game_state_generator=lambda avatar_manager: MockGameState(
            None, MockAvatarManager()
        ),
        communicator=communicator,
        port="0000",
        turn_collector=turn_collector,
    )
    return GameAPI(
        game_state=game_runner.game_state,
        application=app,
        socketio_server=socketio_server,
        activity_monitor=MagicMock(),
    )


@pytest.fixture
def client(app, aiohttp_client, loop):
    return loop.run_until_complete(aiohttp_client(app))
