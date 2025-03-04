from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from gg2haxxy25.common.enums import ContractType, GameClass


class Contract(SQLModel, table=True):
    identifier: UUID = Field(default=None, primary_key=True)
    contract_type: ContractType
    value: int
    target_value: int
    game_class: GameClass

    user_identifier: UUID = Field(default=None, foreign_key="user.identifier")
    user: "User" = Relationship(back_populates="contracts")  # noqa: F821
