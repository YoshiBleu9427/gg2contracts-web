from contracts.common.logging import logger
from contracts.common.settings import settings
from contracts.gg2.tcpserver import setup_server


def main():
    logger.info("Setting up server...")
    server = setup_server(settings.gg2_host, settings.gg2_port)
    logger.info(f"Ready to serve on {settings.gg2_host}:{settings.gg2_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Exited by KeyboardInterrupt")
    except:
        logger.error("Exited by error")
        raise
