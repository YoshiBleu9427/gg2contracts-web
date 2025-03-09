import logging
from io import BytesIO
from socket import socket
from socketserver import StreamRequestHandler, ThreadingTCPServer

from gg2haxxy25.gg2.messagehandler import MessageHandler

MAX_BUF_SIZE = 64 * 1024


logger = logging.getLogger(__name__)


class Handler(StreamRequestHandler):
    def handle(self) -> None:
        self.request: socket

        logger.info(f"{self.client_address} - Got connection")
        handler = MessageHandler()

        while handler.expecting_data:
            logger.debug(f"{self.client_address} - Awaiting data")
            data = self.request.recv(MAX_BUF_SIZE)
            logger.debug(f"{self.client_address} - Handling:")
            response = handler.handle_data(BytesIO(data))
            self.request.sendall(response)

        self.request.close()


def setup_server(host: str, port: int) -> ThreadingTCPServer:
    server = ThreadingTCPServer((host, port), Handler)
    return server
