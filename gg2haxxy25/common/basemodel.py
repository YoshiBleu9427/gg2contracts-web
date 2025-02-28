from pydantic import BaseModel
from typing import Self


class AppBaseModel(BaseModel):
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def from_bytes(data: bytes) -> Self:
        raise NotImplementedError
