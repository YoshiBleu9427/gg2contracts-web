from io import BytesIO
from socket import socket
from socketserver import StreamRequestHandler, ThreadingTCPServer

from gg2haxxy25.gg2.messagehandler import MessageHandler

MAX_BUF_SIZE = 64 * 1024

# TODO replace print with logger


class Handler(StreamRequestHandler):
    def handle(self):
        self.request: socket

        print(f"{self.client_address} - Got connection")
        handler = MessageHandler()

        while handler.expecting_data:
            print(f"{self.client_address} - Awaiting data")
            data = self.request.recv(MAX_BUF_SIZE)
            print(f"{self.client_address} - Handling:")
            response = handler.handle_data(BytesIO(data))
            self.request.sendall(response)

        self.request.close()


def setup_server(host: str, port: int) -> ThreadingTCPServer:
    server = ThreadingTCPServer((host, port), Handler)
    return server
