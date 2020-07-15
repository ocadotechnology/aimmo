import pytest

from simulation.django_communicator import (
    DjangoCommunicator,
    GameMetadataFetchFailedError,
)

from .mock_communicator import DUMMY_GAME_METADATA


async def test_get_users_500_handled_correctly(loop, mock_aioresponse):
    django_api_url = "http://django-api.url"
    mock_aioresponse.get(
        f"{django_api_url}users", status=500, body="<p>Server error</p>"
    )
    communicator = DjangoCommunicator(django_api_url)
    with pytest.raises(GameMetadataFetchFailedError):
        await communicator.get_game_metadata()


async def test_get_users_metadata_success(loop, mock_aioresponse):
    django_api_url = "http://django-api.url"
    mock_aioresponse.get(
        f"{django_api_url}users", status=200, payload=DUMMY_GAME_METADATA
    )
    communicator = DjangoCommunicator(django_api_url)
    response = await communicator.get_game_metadata()
    assert response == DUMMY_GAME_METADATA


async def test_get_users_metadata_cannot_connect_to_server(loop, mock_aioresponse):
    django_api_url = "http://django-api.url"
    communicator = DjangoCommunicator(django_api_url)
    with pytest.raises(GameMetadataFetchFailedError):
        await communicator.get_game_metadata()
