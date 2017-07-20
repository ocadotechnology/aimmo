import socket
import re
import sys

from time import sleep
from subprocess import call

import signal
import sys
import json

class ConnectionProxy():
    """
        A ConnectionProxy is a class that can be binded to another class
        and is supposed to be process a received request and return a
        specific response.

        The default apply function does return the same response as the
        received one.
    """
    def __init__(self, binder):
        self.binder = binder
    def apply(self, received):
        return received


class MockServer():
    """
        Lightweight csocket server used for test_backend:
        * uses simple sockets to mock the Django part of the application.
        * listens to a custom client that can be configured at initialization
        * one can register a "ConnectionProxy" and the server runns them in
          them in the order they have been registered
    """
    def __register_connection(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allows reuse of the socket once the process gets stopped
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #bind the connection
        self.sock.bind((host, port))

        #listen to one client
        self.sock.listen(1)

    def __init__(self, host="localhost", port=8000):
        self.__register_connection(host, port)
        self.runners = []

    def register_proxy(self, runner):
        self.runners.append(runner)

    def clear_proxies(self):
        self.runners = []

    # for the moment supports only gets
    def receive(self):
        def receive_lines(csock):
            raw_request = csock.recv(1024)
            lines = raw_request.split('\n')
            return raw_request, lines[0]

        raw_request, get_request = receive_lines(self.csock)
        resource_identifier = get_request.split(' ')[1]

        return raw_request, resource_identifier

    def serve(self):
        received, received_formatted = self.receive()

        ans = received_formatted
        for runner in self.runners:
            ans = runner.apply(ans)
        return ans

    def run(self, times=1000):
        #listen for connection
        while times > 0:
            self.csock, self.caddr = self.sock.accept()

            # serve the connection
            str_ans = self.serve()
            # print("Responding: " + str_ans)
            self.csock.send("HTTP/1.0 200 OK\nContent-Type: text/plain\n\n" + str_ans)

            times -= 1
            self.csock.close()

if __name__ == "__main__":
    server = MockServer()
    server.run()
