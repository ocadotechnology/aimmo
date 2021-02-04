"""
Any helper functions used for the game.
"""
from __future__ import absolute_import

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from kubernetes.client.api.custom_objects_api import CustomObjectsApi
from kubernetes.client.api_client import ApiClient

from aimmo import app_settings, exceptions

from .models import Game


def render_game(request, game):
    """
    :param request: Request object used to generate this response.
    :param game: Game object.
    :return: HttpResponse object with a given context dictionary and a template.
    """
    context = {
        "current_user_player_key": request.user.pk,
        "active": game.is_active,
        "static_data": game.static_data or "{}",
    }

    return render(request, "players/game_ide.html", context)


def get_environment_connection_settings(game_id):
    """
    This function will return the correct URL parts and a SSL flag
    based on the environment of which it exists in.

    :param game_id: Integer with the ID of the game.
    :return: A dict object with all relevant settings.
    """
    return {
        "game_url_base": get_games_url_base(game_id),
        "game_ssl_flag": app_settings.GAME_SERVER_SSL_FLAG,
        "game_id": game_id,
    }


def get_games_url_base(game_id: int) -> str:
    api_client = ApiClient()
    api_instance = CustomObjectsApi(api_client)
    result = api_instance.list_namespaced_custom_object(
        group="agones.dev",
        version="v1",
        namespace="default",
        plural="gameservers",
        label_selector=f"game-id={game_id}",
    )
    try:
        game_server_status = result["items"][0]["status"]
        return f"http://{game_server_status['address']}:{game_server_status['ports'][0]['port']}"
    except (KeyError, IndexError):
        raise Http404


def get_avatar_id_from_user(user, game_id):
    """
    A helper function which will return an avatar ID that is assigned to a
    particular django user owner in a game.
    :param user: A django user object taken from the request.
    :param game_id: The game ID in which the avatar is being requested from.
    :return: An integer containing the avatar_ID.
    """

    game = get_object_or_404(Game, id=game_id)
    if not game.can_user_play(user):
        raise exceptions.UserCannotPlayGameException

    avatar = game.avatar_set.get(owner=user.id)

    return avatar.id
