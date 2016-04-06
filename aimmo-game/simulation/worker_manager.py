import logging
import requests
import threading
import time

LOGGER = logging.getLogger(__name__)

class WorkerManager(threading.Thread):
    daemon = True

    def __init__(self, game_state, users_url):
        self.game_state = game_state
        self.users_url = users_url
        self.user_codes = {}
        super(WorkerManager, self).__init__()

    def run(self):
        while True:
            try:
                game_data = requests.get(self.users_url).json()
            except (requests.RequestException, ValueError) as err:
                LOGGER.error("Obtaining game data failed: %s", err)
            else:
                game = game_data['main']
                for user in game['users']:
                    print 'user_codes', self.user_codes.keys()
                    print user['id'], 'old_code', self.user_codes.get(user['id'], None), 'new_code', user['code']
                    if self.user_codes.get(user['id'], None) != user['code']:
                        # Remove avatar from the game, so it stops being called for turns
                        self.game_state.remove_avatar(user['id'])
                        # Get persistent state from worker
                        # TODO
                        # Kill worker
                        # TODO
                        # Spawn worker
                        worker_url = 'http://localhost:%d' % (5000 + int(user['id'])) # Comes from spawning
                        # TODO
                        # Initialise worker
                        requests.post("%s/initialise/" % worker_url, json={
                            'code': user['code'],
                            'options': {},
                        })
                        # Add avatar back into game
                        self.game_state.add_avatar(user_id=user['id'], worker_url="%s/turn/" % worker_url)
                        self.user_codes[user['id']] = user['code']

            time.sleep(10)
