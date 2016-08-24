from django.conf import settings
import subprocess
import os


def get_url(game):
    if os.environ.get('AIMMO_MODE', '') == 'minikube':
        output = subprocess.check_output(['./test-bin/minikube', 'service', 'game-%s' % game, '--url'])
        return (output.strip(), '/game/%s/socket.io' % game)
    else:
        return ('http://localhost:5000', '/socket.io')


#: URL function for locating the game server, takes one parameter `game`
GAME_SERVER_LOCATION_FUNCTION = getattr(
    settings,
    'AIMMO_GAME_SERVER_LOCATION_FUNCTION',
    get_url
)
