class LogCollector:
    def __init__(self, ):
        super(LogCollector, self).__init__()

        self.player_logs = None

    def set_end_turn_callback(self, callback_method):
        self._end_turn_callback = callback_method
