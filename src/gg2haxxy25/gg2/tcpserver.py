from io import BytesIO
from socket import socket
from socketserver import StreamRequestHandler, ThreadingTCPServer

from gg2haxxy25.gg2.messagehandler import MessageHandler

MAX_BUF_SIZE = 64 * 1024


class Handler(StreamRequestHandler):
    def handle(self):
        self.request: socket

        handler = MessageHandler()

        while handler.expecting_data:
            data = self.request.recv(MAX_BUF_SIZE)
            response = handler.handle_data(BytesIO(data))
            self.request.sendall(response)

        self.request.close()


def setup_server(host: str, port: int) -> ThreadingTCPServer:
    server = ThreadingTCPServer((host, port), Handler)
    return server
