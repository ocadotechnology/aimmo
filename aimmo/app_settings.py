from django.conf import settings

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_URL_FUNCTION = getattr(settings, "AIMMO_GAME_SERVER_URL_FUNCTION", None)
GAME_SERVER_PORT_FUNCTION = getattr(settings, "AIMMO_GAME_SERVER_PORT_FUNCTION", None)
GAME_SERVER_SSL_FLAG = getattr(settings, "AIMMO_GAME_SERVER_SSL_FLAG", False)

# Hostname for django server to pass onto a game server
DJANGO_BASE_URL_FOR_GAME_SERVER = getattr(settings, "AIMMO_DJANGO_BASE_URL", "localhost")

MAX_LEVEL = 1
