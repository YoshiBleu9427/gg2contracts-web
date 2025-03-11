from contracts.gg2.tcpserver import setup_server


def main():
    print("Setting up server...")
    server = setup_server("localhost", 4646)  # TODO env vars
    print("Ready to serve on localhost:4646")
    server.serve_forever()
