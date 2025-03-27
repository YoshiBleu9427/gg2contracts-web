from contracts.common.settings import settings
from contracts.gg2.tcpserver import setup_server


def main():
    print("Setting up server...")
    server = setup_server(settings.gg2_host, settings.gg2_port)
    print(f"Ready to serve on {settings.gg2_host}:{settings.gg2_port}")
    server.serve_forever()
