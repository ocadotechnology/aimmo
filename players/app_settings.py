from django.conf import settings


#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_LOCATION_FUNCTION = getattr(
    settings,
    'AIMMO_GAME_SERVER_LOCATION_FUNCTION',
    lambda _: ('http://localhost:5000', '/socket.io'),
)
