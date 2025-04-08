import struct
from uuid import UUID


def uchar(value: int) -> bytes:
    return struct.pack("<B", value)


def ushort(value: int) -> bytes:
    return struct.pack("<H", value)


def uint(value: int) -> bytes:
    return struct.pack("<I", value)


def uuid(value: UUID) -> bytes:
    return value.bytes


def short_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    assert len(encoded) < 2 ^ 8
    return uchar(len(encoded)) + encoded


def long_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    assert len(encoded) < 2 ^ 16
    return ushort(len(encoded)) + encoded
