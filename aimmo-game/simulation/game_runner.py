import time
import threading

WORKER_UPDATE_SLEEP_TIME = 5


class GameRunner(threading.Thread):
    def __init__(self, worker_manager, turn_manager, game_state, communicator):
        super(GameRunner, self).__init__()
        self.worker_manager = worker_manager
        self.turn_manager = turn_manager
        self.game_state = game_state
        self.communicator = communicator

    def get_users_to_add(self, game_metadata):
        def user_is_new(user):
            return user['id'] not in self.worker_manager.avatar_id_to_worker.keys()

        return [user['id'] for user in game_metadata['users'] if user_is_new(user)]

    def get_users_to_delete(self, game_metadata):
        def is_stale(user_id):  # is user in worker but not game metadata
            return user_id not in [user['id'] for user in game_metadata['users']]

        return [user_id for user_id in self.worker_manager.avatar_id_to_worker.keys() if is_stale(user_id)]

    def update_main_user(self, game_metadata):
        self.game_state.main_avatar_id = game_metadata['main_avatar']

    def run(self):
        while True:
            game_metadata = self.communicator.get_game_metadata()['main']

            users_to_add = self.get_users_to_add(game_metadata)
            users_to_delete = self.get_users_to_delete(game_metadata)

            worker_urls = self.worker_manager.add_workers(users_to_add)
            self.worker_manager.delete_workers(users_to_delete)
            self.game_state.add_avatars(users_to_add, worker_urls)
            self.game_state.delete_avatars(users_to_delete)
            self.worker_manager.update_worker_codes(game_metadata['users'])

            self.update_main_user(game_metadata)

            time.sleep(WORKER_UPDATE_SLEEP_TIME)
