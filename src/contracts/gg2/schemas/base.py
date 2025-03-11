import socket
from typing import Self


class GG2Serializable:
    def to_bytes(self) -> bytes:
        raise NotImplementedError


class GG2Deserializable:
    @classmethod
    def from_bytes(cls, s: socket.socket) -> Self:
        raise NotImplementedError
