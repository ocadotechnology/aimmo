class LogManager(object):
    """ Wrapper for the PrintCollector which allows logs to have
        state. The class definition for the PrintCollector is
        passed into the globals for the user's code before execution. """

    def __init__(self):
        class PrintCollector(object):
            """ Collect written text, and return it when called. """

            def __init__(print_collector, _getattr_=None):
                print_collector.logs = self.logs
                print_collector._getattr_ = _getattr_

            def write(print_collector, text):
                print_collector.logs.append(text)

            def __call__(print_collector):
                return "".join(print_collector.logs)

            def _call_print(print_collector, *objects, **kwargs):
                if kwargs.get("file", None) is None:
                    kwargs["file"] = print_collector
                else:
                    print_collector._getattr_(kwargs["file"], "write")

                print(*objects, **kwargs)

        self.logs = []
        self.print_collector = PrintCollector

    def get_print_collector(self):
        return self.print_collector

    def get_logs(self):
        return "".join(self.logs)

    def is_empty(self):
        return self.logs == []

    def clear_logs(self):
        self.logs = []
