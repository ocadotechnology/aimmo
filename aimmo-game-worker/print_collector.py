class PrintCollectorState(object):

    def __init__(self):
        self.logs = []

        class PrintCollector(object):
            """Collect written text, and return it when called."""

            def __init__(print_collector_self, _getattr_=None):
                print_collector_self.logs = self.logs
                print_collector_self._getattr_ = _getattr_

            def write(print_collector_self, text):
                print_collector_self.logs.append(text)

            def __call__(print_collector_self):
                return ''.join(print_collector_self.logs)

            def _call_print(print_collector_self, *objects, **kwargs):
                if kwargs.get('file', None) is None:
                    kwargs['file'] = print_collector_self
                else:
                    print_collector_self._getattr_(kwargs['file'], 'write')

                print(*objects, **kwargs)
        
        self.print_collector = PrintCollector

    def get_print_collector(self):
        return self.print_collector
    
    def get_logs(self):
        return self.logs

    def clear_logs(self):
        self.logs = []