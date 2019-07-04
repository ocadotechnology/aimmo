import asyncio
from unittest import TestCase

import pytest
from aioresponses import aioresponses
from requests import Response
from tests.test_simulation.concrete_worker import ConcreteWorker

import mock
from simulation.workers.worker import Worker

DEFAULT_RESPONSE_CONTENT = (
    b'{"action": "test_action",' b'"log": "test_log",' b'"avatar_updated": "True"}'
)

MISSING_KEY_RESPONSE_CONTENT = (
    b'{"corruptedKey": "test_action",'
    b'"log": "test_log",'
    b'"avatar_updated": "True"}'
)


def construct_test_response(status_code=200, response_content=DEFAULT_RESPONSE_CONTENT):
    post_response = Response()
    post_response.status_code = status_code
    post_response._content = response_content
    return post_response


@pytest.fixture
def worker():
    return ConcreteWorker(1, 0)


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mocked:
        yield mocked


@pytest.mark.asyncio
async def test_fetch_data_fetches_correct_response(mock_aioresponse, worker):
    mock_aioresponse.post(
        "http://test/turn/", status=200, body=DEFAULT_RESPONSE_CONTENT
    )
    await asyncio.ensure_future(worker.fetch_data(state_view={}))

    assert worker.serialized_action == "test_action"
    assert worker.log == "test_log"
    assert worker.has_code_updated == "True"


def test_setting_defaults_works_correctly(worker):
    worker.log = "test_log_fake"
    worker.serialised_action = "test_action_fake"
    worker.has_code_updated = "test_avatar_updated_fake"

    worker._set_defaults()

    assert worker.serialized_action is None
    assert worker.log is None
    assert worker.has_code_updated is False


@pytest.mark.asyncio
async def test_fetch_data_cannot_connect_to_worker(mock_aioresponse, worker, mocker):
    mocker.patch.object(target=Worker, attribute="_set_defaults")
    mock_aioresponse.post(
        "http://test/turn/", status=500, body=MISSING_KEY_RESPONSE_CONTENT
    )
    await asyncio.ensure_future(worker.fetch_data(state_view={}))

    worker._set_defaults.assert_called_once()


@pytest.mark.asyncio
async def test_missing_key_in_worker_data(mock_aioresponse, worker, mocker):
    mocker.patch.object(target=Worker, attribute="_set_defaults")
    mock_aioresponse.post(
        "http://test/turn/", status=200, body=MISSING_KEY_RESPONSE_CONTENT
    )
    await asyncio.ensure_future(worker.fetch_data(state_view={}))

    worker._set_defaults.assert_called_once()
