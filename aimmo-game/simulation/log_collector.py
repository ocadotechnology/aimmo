class LogCollector:
    """
    This class aggregates:
    - the avatar logs (logs outputted by the game under certain conditions)
    These logs are concatenated to form the `playerLogs`.
    """

    def __init__(self, avatar_manager):
        super(LogCollector, self).__init__()

        self.avatar_manager = avatar_manager

    def collect_logs(self, user_id):
        avatar = self.avatar_manager.get_avatar(user_id)

        return "\n".join(avatar.logs)
