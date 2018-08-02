class LogsProvider(object):
    """
    A mapping from avatar.player_id to their most recent logs. Is thread safe.
    """
    def __init__(self):
        self._logs = {}

    def set_user_logs(self, user_id, logs):
        self._logs[user_id] = logs
