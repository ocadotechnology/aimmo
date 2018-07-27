"""
Any helper functions used for the unity game.
"""

from django.shortcuts import render, get_object_or_404
from aimmo import app_settings, exceptions
from models import Game


def render_game(request, game):
    """
    :param request: Request object used to generate this response.
    :param game: Game object.
    :return: HttpResponse object with a given context dictionary and a template.
    """
    context = {'current_user_player_key': request.user.pk, 'active': game.is_active,
               'static_data': game.static_data or '{}'
               }

    connection_settings = get_environment_connection_settings(game.id)

    context.update(connection_settings)

    return render(request, 'players/game_ide.html', context)


def get_environment_connection_settings(game_id):
    """
    This function will return the correct URL parts and a SSL flag
    based on the environment of which it exists in.

    :param request: Request object used to generate this response.
    :param game_id: Integer with the ID of the game.
    :return: A dict object with all relevant settings.
    """

    return {
        'game_url_base': app_settings.GAME_SERVER_URL_FUNCTION(game_id)[0],
        'game_url_path': app_settings.GAME_SERVER_URL_FUNCTION(game_id)[1],
        'game_url_port': app_settings.GAME_SERVER_PORT_FUNCTION(game_id),
        'game_ssl_flag': app_settings.GAME_SERVER_SSL_FLAG, 'game_id': game_id
    }


def get_avatar_id_from_user_id(django_user_id, game_id):
    """
    A helper function which will return an avatar ID that is assigned to a
    particular django user owner in a game.
    :param django_user_id: A django user ID taken from the request.
    :param game_id: The game ID in which the avatar is being requested from.
    :return: An integer containing the avatar_ID.
    """
    game = get_object_or_404(Game, id=game_id)

    if not game.can_user_play(django_user_id):
        raise exceptions.UserCannotPlayGameException

    avatar = game.avatar_set.get(owner=django_user_id)

    return avatar.id
