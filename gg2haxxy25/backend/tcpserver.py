from socketserver import TCPServer, StreamRequestHandler


class Handler(StreamRequestHandler):
    def handle(self):
        self.data: bytes = self.request.recv(1024).strip()
        print("From {}".format(self.client_address[0]))
        print(self.data)

        self.request.sendall(self.data.upper())


def setup_server(host: str, port: int) -> TCPServer:
    server = TCPServer((host, port), Handler)
    return server
