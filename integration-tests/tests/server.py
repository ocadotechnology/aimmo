import socket
import re
import sys

from time import sleep
from subprocess import call


################################################################################

# Register custom mockery...

# import sys
# # Add the ptdraft folder path to the sys.path list
# sys.path.append('../../')
#
# import importlib
# mockery = importlib.import_module("aimmo-game-creator.tests.test_worker_manager")


################################################################################

import signal
import sys
import json

################################################################################

# register a specific signal handler if necessary at the termination of the program
# def signal_handler(signal, frame):
    # close the socket here
    # sys.exit(0)
# signal.signal(signal.SIGINT, signal_handler)

################################################################################

class Runner():
    def apply(self, received):
        return received

################################################################################

# Class that receives a mock(as in unit tests) and creates a lightweight server
# at localhost
class MockServer():
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

        print "Server starting on port " + str(port)

    def __init__(self, host="localhost", port=8000):
        self.__register_connection(host, port)
        self.runners = []

    # to implement runners...
    def register_runner(self, runner):
        self.runners.append(runner)

    def receive(self):
        def receive_lines(csock):
            req = csock.recv(1024)
            lines = req.split('\n')
            return lines

        get_request = receive_lines(self.csock)[0]
        resource_identifier = get_request.split(' ')[1]

        return resource_identifier

    def serve(self):
        received = self.receive()
        print "Received request " + received

        ans = received
        for runner in self.runners:
            ans = runner.apply(ans)
        return ans

    def run(self):
        #listen for connection
        while True:
            self.csock, self.caddr = self.sock.accept()
            print "Connection from:" + `self.caddr`

            # serve the connection
            self.serve()

if __name__ == "__main__":
    server = MockServer()
    server.run()
