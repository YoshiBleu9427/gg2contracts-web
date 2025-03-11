import socket
from uuid import UUID

from pydantic import BaseModel

from contracts.gg2.network import read
from contracts.gg2.schemas.base import GG2Deserializable


class InPlayerContractUpdate(BaseModel, GG2Deserializable):
    contract_id: UUID
    value_modifier: int

    @classmethod
    def from_bytes(cls, s: socket.socket):
        contract_id = read.uuid(s)
        value_mod = read.uchar(s)
        return InPlayerContractUpdate(contract_id=contract_id, value_modifier=value_mod)


class InPlayerRoundEndData(BaseModel, GG2Deserializable):
    session_token: UUID
    contracts: list[InPlayerContractUpdate]

    @classmethod
    def from_bytes(cls, s: socket.socket):
        session_token = read.uuid(s)
        contract_count = read.uchar(s)
        contracts = [
            InPlayerContractUpdate.from_bytes(s) for _ in range(contract_count)
        ]

        return InPlayerRoundEndData(session_token=session_token, contracts=contracts)
