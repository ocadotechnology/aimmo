class LogCollector:
    def __init__(self,):
        super(LogCollector, self).__init__()

        self.player_logs = None
        self.worker = None
        self.avatar = None

    def should_send_logs(self):
        return bool(self.player_logs)

    def collect_logs(self):
        self.player_logs = self.worker.log
        if self.avatar.log:
            self.player_logs += self.avatar.log
        return self.player_logs
