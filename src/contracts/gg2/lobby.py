import ipaddress
import socket
from uuid import UUID

from pydantic import BaseModel

from contracts.gg2.network import read, write
from contracts.gg2.schemas.base import GG2Deserializable

LOBBY_UUID = UUID("1ccf16b1436d856f504dcc1af306aaa7")
LOBBY_READ_UUID = UUID("297d0df4430cbf61640a640897eaef57")
LOBBY_SERVER_HOST = "ganggarrison.com"
LOBBY_SERVER_PORT = 29944


class LobbyServerData(BaseModel, GG2Deserializable):
    protocol: int
    server_ip: str
    server_port: int
    slots: int
    players: int
    bots: int
    private: bool

    info: dict[str, str]

    @classmethod
    def from_bytes(cls, s: socket.socket):
        _ = read.read_int(s, big_endian=True)  # serverInfoLen

        protocol = read.byte(s)
        server_port = read.ushort(s, big_endian=True)

        server_ip_int = read.uint(s, big_endian=True)
        server_ip = str(ipaddress.IPv4Address(server_ip_int))

        # ignore ipv6
        read._fetch(s, 18)

        slots = read.ushort(s, big_endian=True)
        players = read.ushort(s, big_endian=True)
        bots = read.ushort(s, big_endian=True)

        flags = read.ushort(s, big_endian=True)
        is_private = (flags & 0x1) != 0

        infos = {}
        info_count = read.ushort(s, big_endian=True)
        for j in range(info_count):
            key = read.short_string(s)
            value = read.long_string(s, big_endian=True)

            infos[key] = value

        return cls(
            protocol=protocol,
            server_port=server_port,
            server_ip=server_ip,
            slots=slots,
            players=players,
            bots=bots,
            private=is_private,
            info=infos,
        )


class LobbyData(BaseModel, GG2Deserializable):
    servers: list[LobbyServerData]

    @classmethod
    def from_bytes(cls, s: socket.socket):
        nb_servers = read.read_int(s, big_endian=True)
        servers = [LobbyServerData.from_bytes(s) for _ in range(nb_servers)]
        return cls(servers=servers)


def _send_lobby_query() -> socket.socket:
    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((LOBBY_SERVER_HOST, LOBBY_SERVER_PORT))
    send_data = write.uuid(LOBBY_READ_UUID) + write.uuid(LOBBY_UUID)
    s.sendall(send_data)
    return s


def get_lobby_data() -> LobbyData:
    s = _send_lobby_query()
    return LobbyData.from_bytes(s)
