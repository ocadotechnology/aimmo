from django.conf import settings
from django.utils.module_loading import import_string
from permissions import default_preview_user
from django.contrib.auth.models import User

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_URL_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_URL_FUNCTION', None)
GAME_SERVER_PORT_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_PORT_FUNCTION', None)
GAME_SERVER_SSL_FLAG = getattr(settings, 'AIMMO_GAME_SERVER_SSL_FLAG', False)
PREVIEW_USER_AIMMO_DECORATOR = getattr(settings, 'PREVIEW_USER_AIMMO_DECORATOR', None)
USERS_FOR_NEW_AIMMO_GAME = getattr(settings, 'USERS_FOR_NEW_AIMMO_GAME', None)


def get_aimmo_preview_user_decorator():
    if PREVIEW_USER_AIMMO_DECORATOR:
        func = import_string(PREVIEW_USER_AIMMO_DECORATOR)
        return func
    return default_preview_user


def get_users_for_new_game(request):
    if USERS_FOR_NEW_AIMMO_GAME:
        func = import_string(USERS_FOR_NEW_AIMMO_GAME)
        return func(request)
    return User.objects.all()


preview_user = get_aimmo_preview_user_decorator()

MAX_LEVEL = 1
