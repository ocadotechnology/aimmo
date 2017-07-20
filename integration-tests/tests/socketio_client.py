# from socketIO_client import SocketIO, LoggingNamespace
#
# class SocketClient():
#     def __init__(self, host, port, path, binder):
#         self.host = host
#         self.port = port
#         self.path = path
#         self.binder = binder
#
#     def on_connect(self):
#         print("Socket io connected")
#
#     def start(self):
#         print("Starting socket io client...")
#
#         self.socket_io = SocketIO(
#             self.host,
#             self.port)
#             # cookies=self.binder.session.cookies)
#         print("Registering listeners...")
#         self.socket_io.on('connect', self.on_connect)
#         self.socket_io.emit('world-update')

import websocket, httplib, sys, asyncore, requests, json
from pprint import pprint

import unicodedata


class SocketClient():
    def __init__(self, host, port, path, binder):
        self.host = host
        self.port = port
        self.path = path
        self.binder = binder

    def start(self):
        def _onopen():
            print("opened!")

        def _onmessage(msg):
            print("msg: " + str(msg))

        def _onclose():
            print("closed!")

        print("Connecting to: %s:%d" %(self.host, self.port))

        conn  = httplib.HTTPConnection('localhost:7001')

        # conn  = httplib.HTTPConnection(self.host + ":" + str(self.port))
        # conn.request('POST','/socket.io/')
        # resp  = conn.getresponse()
        # hskey = resp.read().split(':')[0]

        payload = {}
        payload['csrfmiddlewaretoken']=self.binder.session.cookies['csrftoken']
        where = self.host + ":" + str(self.port) + "/socket.io/"
        print("Request at" + where)
        result = self.binder.session.get(where)

        # TODO: this is awful
        params = result.text.split(':')
        raw = max(params, key=len)
        string = unicodedata.normalize('NFKD', raw).encode('ascii','ignore')
        hskey = string.split('"')[1]

        print("Starting the socket....." + hskey)
        ws = websocket.WebSocket(
                        'ws://localhost:7001/socket.io/websocket/'+hskey,
                        onopen   = _onopen,
                        onmessage = _onmessage,
                        onclose = _onclose)

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            ws.close()
