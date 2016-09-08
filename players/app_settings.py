from django.conf import settings

#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_LOCATION_FUNCTION = getattr(settings, 'AIMMO_GAME_SERVER_LOCATION_FUNCTION', None)

CREATOR_AUTH_TOKEN = getattr(settings, 'CREATOR_AUTH_TOKEN', 'insecure-creator-auth-token')

MAX_LEVEL = 1
