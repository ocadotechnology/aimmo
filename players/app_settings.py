from django.conf import settings

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_URL_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_URL_FUNCTION', None)
GAME_SERVER_PORT_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_PORT_FUNCTION', None)
GAME_SERVER_SSL_FLAG = getattr(settings, 'AIMMO_GAME_SERVER_SSL_FLAG', False)

MAX_LEVEL = 1
