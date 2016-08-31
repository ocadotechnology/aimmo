class SocketLogger(object):
    def __init__(self, socket):
        self.socket = socket

    def write(self, line):
        self.socket.emit('log-line', {'line': line})
