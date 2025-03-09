import logging
from socketserver import ThreadingTCPServer

from gg2haxxy25.gg2.messagehandler import MessageHandler

logger = logging.getLogger(__name__)


def setup_server(host: str, port: int) -> ThreadingTCPServer:
    server = ThreadingTCPServer((host, port), MessageHandler)
    return server
