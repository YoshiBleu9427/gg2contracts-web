import struct
from io import BytesIO
from uuid import UUID


def uchar(b: BytesIO) -> int:
    return struct.unpack("<B", b.read(1))[0]


def ushort(b: BytesIO) -> int:
    return struct.unpack("<H", b.read(2))[0]


def uuid(b: BytesIO) -> UUID:
    return UUID(bytes=b.read(16))


def short_string(b: BytesIO) -> str:
    str_len: int = struct.unpack("<B", b.read(1))[0]
    str_bytes = b.read(str_len)
    return str(str_bytes, "utf-8")


def long_string(b: BytesIO) -> str:
    str_len: int = struct.unpack("<H", b.read(2))[0]
    str_bytes = b.read(str_len)
    return str(str_bytes, "utf-8")
