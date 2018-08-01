"""
Any helper functions used for the unity game.
"""

from django.shortcuts import render
from aimmo import app_settings


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
        'game_url_base': _add_game_port_to_game_base(game_id),
        'game_url_path': app_settings.GAME_SERVER_URL_FUNCTION(game_id)[1],
        'game_ssl_flag': app_settings.GAME_SERVER_SSL_FLAG, 'game_id': game_id
    }


def _add_game_port_to_game_base(game_id):
    game_base = app_settings.GAME_SERVER_URL_FUNCTION(game_id)[0]
    game_port = app_settings.GAME_SERVER_PORT_FUNCTION(game_id)

    if _connection_on_k8s_mode(game_port):
        return game_base

    return "{0}:{1}".format(game_base, game_port)


def _connection_on_k8s_mode(game_port):
    return game_port == 0
