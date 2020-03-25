class LogCollector:
    """
    This class aggregates:
    - the worker logs (logs coming from the worker)
    - the avatar logs (logs outputted by the game under certain conditions)
    These logs are concatenated to form the `player_logs`.
    """

    def __init__(self, worker_manager, avatar_manager):
        super(LogCollector, self).__init__()

        self.worker_manager = worker_manager
        self.avatar_manager = avatar_manager

    def collect_logs(self, user_id):
        worker = self.worker_manager.player_id_to_worker[user_id]
        avatar = self.avatar_manager.get_avatar(user_id)

        player_logs = ""
        for worker_log in worker.logs:
            player_logs += worker_log

        if len(avatar.logs) > 0:
            player_logs += "\n"
            player_logs += "\n".join(avatar.logs)

        return player_logs
