import socket
import struct
import time
from uuid import UUID


def _fetch(s: socket.socket, n: int) -> bytes:
    """
    Reads from the given socket until exactly n bytes have been read.
    """
    i = 0
    need_count = n
    buffer = bytearray()
    while need_count > 0:
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


def uchar(s: socket.socket) -> int:
    return struct.unpack("<B", _fetch(s, 1))[0]


def ushort(s: socket.socket) -> int:
    return struct.unpack("<H", _fetch(s, 2))[0]


def uuid(s: socket.socket) -> UUID:
    return UUID(bytes=_fetch(s, 16))


def short_string(s: socket.socket) -> str:
    str_len: int = struct.unpack("<B", _fetch(s, 1))[0]
    str_bytes = _fetch(s, str_len)
    return str(str_bytes, "utf-8")


def long_string(s: socket.socket) -> str:
    str_len: int = struct.unpack("<H", _fetch(s, 2))[0]
    str_bytes = _fetch(s, str_len)
    return str(str_bytes, "utf-8")
