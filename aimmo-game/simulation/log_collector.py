class LogCollector:
    """
    This class aggregates:
    - the worker logs (logs created from print statements in the user's code)
    - the avatar logs (logs outputted by the game under certain conditions)
    These logs are concatenated to form the `player_logs`.
    """

    def __init__(self, worker_manager, avatar_manager):
        super(LogCollector, self).__init__()

        self.player_logs = None
        self.worker_manager = worker_manager
        self.avatar_manager = avatar_manager

    def collect_logs(self, user_id):
        worker = self.worker_manager.player_id_to_worker[user_id]
        avatar = self.avatar_manager.get_avatar(user_id)

        self.player_logs = worker.log
        for log in avatar.logs:
            self.player_logs += log

        return self.player_logs
