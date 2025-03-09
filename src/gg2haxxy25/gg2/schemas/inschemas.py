from io import BytesIO
from uuid import UUID

from pydantic import BaseModel

from gg2haxxy25.gg2.network import read
from gg2haxxy25.gg2.schemas.base import GG2Deserializable


class InPlayerContractUpdate(BaseModel, GG2Deserializable):
    contract_id: UUID
    value_modifier: int

    @classmethod
    def from_bytes(cls, data: BytesIO):
        contract_id = read.uuid(data)
        value_mod = read.uchar(data)
        return InPlayerContractUpdate(contract_id=contract_id, value_modifier=value_mod)


class InPlayerRoundEndData(BaseModel, GG2Deserializable):
    challenge_token: UUID
    contracts: list[InPlayerContractUpdate]

    @classmethod
    def from_bytes(cls, data: BytesIO):
        challenge_token = read.uuid(data)
        contract_count = read.uchar(data)
        contracts = [
            InPlayerContractUpdate.from_bytes(data) for _ in range(contract_count)
        ]

        return InPlayerRoundEndData(
            challenge_token=challenge_token, contracts=contracts
        )
