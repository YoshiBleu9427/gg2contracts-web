import socket
import struct
import time
from uuid import UUID

from contracts.common.settings import settings


def _endianness(big_endian):
    if big_endian:
        return ">"
    return "<"


def _fetch(s: socket.socket, n: int) -> bytes:
    """
    Reads from the given socket until exactly n bytes have been read.
    """
    i = 0
    need_count = n
    buffer = bytearray()

    while need_count > 0:
        s.settimeout(settings.gg2_timeout)
        this_read_buf = s.recv(need_count)

        this_read_count = len(this_read_buf)
        need_count -= this_read_count
        buffer += this_read_buf

        i += 1
        if i > 10:
            raise TimeoutError
        if i > 5:
            time.sleep(0.1 * i)

    return bytes(buffer)


def byte(s: socket.socket) -> int:
    return int(_fetch(s, 1)[0])


def uchar(s: socket.socket) -> int:
    return struct.unpack("<B", _fetch(s, 1))[0]


def ushort(s: socket.socket, big_endian=False) -> int:
    return struct.unpack(f"{_endianness(big_endian)}H", _fetch(s, 2))[0]


def uint(s: socket.socket, big_endian=False) -> int:
    return struct.unpack(f"{_endianness(big_endian)}I", _fetch(s, 4))[0]


def uuid(s: socket.socket) -> UUID:
    return UUID(bytes=_fetch(s, 16))


def short_string(s: socket.socket) -> str:
    str_len: int = struct.unpack("<B", _fetch(s, 1))[0]
    str_bytes = _fetch(s, str_len)
    try:
        return str(str_bytes, "utf-8")
    except UnicodeDecodeError:
        return str_bytes.hex()


def long_string(s: socket.socket, big_endian=False) -> str:
    str_len: int = struct.unpack(f"{_endianness(big_endian)}H", _fetch(s, 2))[0]
    str_bytes = _fetch(s, str_len)
    try:
        return str(str_bytes, "utf-8")
    except UnicodeDecodeError:
        return str_bytes.hex()


def read_int(s: socket.socket, big_endian=False) -> int:
    return struct.unpack(f"{_endianness(big_endian)}i", _fetch(s, 4))[0]
