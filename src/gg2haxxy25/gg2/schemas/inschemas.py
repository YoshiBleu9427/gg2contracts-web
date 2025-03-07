from io import BytesIO
from typing import Self
from uuid import UUID

from pydantic import BaseModel

from gg2haxxy25.common.enums import GameClass
from gg2haxxy25.gg2.network import read
from gg2haxxy25.gg2.schemas.base import GG2Deserializable


class ServerGameData(BaseModel, GG2Deserializable):
    challenge: UUID
    kills_as: dict[GameClass, int]
    kills_against: dict[GameClass, int]

    @classmethod
    def from_bytes(cls, data: BytesIO) -> Self:
        raise NotImplementedError


class GG2InContractData(BaseModel, GG2Deserializable):
    contract_id: UUID
    value_modifier: int

    @classmethod
    def from_bytes(cls, data: BytesIO):
        contract_id = read.uuid(data)
        value_mod = read.uchar(data)
        return GG2InContractData(contract_id=contract_id, value_modifier=value_mod)


class GG2InContractUserData(BaseModel, GG2Deserializable):
    challenge_token: UUID
    contracts: list[GG2InContractData]

    @classmethod
    def from_bytes(cls, data: BytesIO):
        challenge_token = read.uuid(data)
        contract_count = read.uchar(data)
        contracts = [GG2InContractData.from_bytes(data) for _ in range(contract_count)]

        return GG2InContractUserData(
            challenge_token=challenge_token, contracts=contracts
        )
