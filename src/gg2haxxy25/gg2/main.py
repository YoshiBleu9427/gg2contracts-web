from gg2.tcpserver import setup_server


def main():
    server = setup_server("localhost", 4646)  # TODO env vars
    server.serve_forever()


if __name__ == "__main__":
    main()
