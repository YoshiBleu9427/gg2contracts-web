from typing import Self
from uuid import UUID

from pydantic import BaseModel
from pydantic.fields import Field

from contracts.common.enums import ContractType, GameClass
from contracts.common.models import Contract, Reward
from contracts.gg2.network import write
from contracts.gg2.schemas.base import GG2Serializable


class GG2OutRewards(BaseModel, GG2Serializable):
    rewards: list[Reward]

    def to_bytes(self) -> bytes:
        return write.long_string(":".join([r.name for r in self.rewards]))


class GG2OutContract(BaseModel, GG2Serializable):
    identifier: UUID
    contract_type: ContractType
    value: int = Field(ge=0, lt=256)
    target_value: int = Field(ge=0, lt=256)
    game_class: GameClass
    points: int = Field(ge=0, lt=256)

    @classmethod
    def from_contract(cls, contract: Contract) -> Self:
        return cls(**contract.model_dump(include=cls.model_fields.keys()))  # type: ignore

    def to_bytes(self) -> bytes:
        return (
            write.uuid(self.identifier)
            + write.uchar(self.contract_type.value)
            + write.uchar(self.value)
            + write.uchar(self.target_value)
            + write.uchar(self.game_class.value)
            + write.uchar(self.points)
        )


class GG2OutNewContract(BaseModel, GG2Serializable):
    identifier: UUID
    contract_type: ContractType
    target_value: int = Field(ge=0, lt=256)
    game_class: GameClass
    points: int = Field(ge=0, lt=256)

    @classmethod
    def from_contract(cls, contract: Contract) -> Self:
        return cls(**contract.model_dump(include=cls.model_fields.keys()))  # type: ignore

    def to_bytes(self) -> bytes:
        return (
            write.uuid(self.identifier)
            + write.uchar(self.contract_type.value)
            + write.uchar(self.target_value)
            + write.uchar(self.game_class.value)
            + write.uchar(self.points)
        )


class GG2OutContractUpdateData(BaseModel, GG2Serializable):
    session_token: UUID
    completed_contract_ids: list[UUID]
    new_contracts: list[GG2OutNewContract]

    def to_bytes(self) -> bytes:
        buffer = bytearray()

        buffer += write.uuid(self.session_token)

        buffer += write.uchar(len(self.completed_contract_ids))
        for completed_contract in self.completed_contract_ids:
            buffer += write.uuid(completed_contract)

        buffer += write.uchar(len(self.new_contracts))
        for new_contract in self.new_contracts:
            buffer += new_contract.to_bytes()

        return bytes(buffer)
