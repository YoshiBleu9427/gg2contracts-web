import logging
from socketserver import ThreadingTCPServer

from contracts.gg2.messagehandler import MessageHandler

logger = logging.getLogger(__name__)


def setup_server(host: str, port: int) -> ThreadingTCPServer:
    server = ThreadingTCPServer((host, port), MessageHandler)
    return server
