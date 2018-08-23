import time
import threading

WORKER_UPDATE_SLEEP_TIME = 10


class GameRunner(threading.Thread):
    def __init__(self, worker_manager, game_state, communicator):
        super(GameRunner, self).__init__()
        self.worker_manager = worker_manager
        self.game_state = game_state
        self.communicator = communicator

    def get_users_to_add(self, game_metadata):
        def player_is_new(_player):
            return _player['id'] not in self.worker_manager.avatar_id_to_worker.keys()

        return [player['id'] for player in game_metadata['users'] if player_is_new(player)]

    def get_users_to_delete(self, game_metadata):
        def player_in_worker_manager_but_not_metadata(pid):
            return pid not in [player['id'] for player in game_metadata['users']]

        return [player_id for player_id in self.worker_manager.avatar_id_to_worker.keys()
                if player_in_worker_manager_but_not_metadata(player_id)]

    def update_main_user(self, game_metadata):
        self.game_state.main_avatar_id = game_metadata['main_avatar']

    def update(self):
        game_metadata = self.communicator.get_game_metadata()['main']

        users_to_add = self.get_users_to_add(game_metadata)
        users_to_delete = self.get_users_to_delete(game_metadata)

        worker_urls = self.worker_manager.add_workers(users_to_add)
        self.worker_manager.delete_workers(users_to_delete)
        self.game_state.add_avatars(users_to_add, worker_urls)
        self.game_state.delete_avatars(users_to_delete)
        self.worker_manager.update_worker_codes(game_metadata['users'])

        self.update_main_user(game_metadata)

    def run(self):
        while True:
            self.update()
            time.sleep(WORKER_UPDATE_SLEEP_TIME)
