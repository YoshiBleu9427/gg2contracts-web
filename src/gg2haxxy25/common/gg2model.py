from typing import Self


class GG2Model:
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def from_bytes(data: bytes) -> Self:
        raise NotImplementedError
