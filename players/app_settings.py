from django.conf import settings
from django.utils.module_loading import import_string
from permissions import default_preview_user

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_URL_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_URL_FUNCTION', None)
GAME_SERVER_PORT_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_PORT_FUNCTION', None)
GAME_SERVER_SSL_FLAG = getattr(settings, 'AIMMO_GAME_SERVER_SSL_FLAG', False)
PREVIEW_USER_AIMMO_DECORATOR = getattr(settings, 'PREVIEW_USER_AIMMO_DECORATOR', None)


def get_aimmo_preview_user_decorator():
    if PREVIEW_USER_AIMMO_DECORATOR:
        func = import_string(PREVIEW_USER_AIMMO_DECORATOR)
        return func
    else:
        return default_preview_user


preview_user = get_aimmo_preview_user_decorator()


MAX_LEVEL = 1
