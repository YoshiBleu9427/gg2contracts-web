from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from gg2haxxy25.common.enums import GameClass
from gg2haxxy25.common.models.contract import Contract


class User(SQLModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username: str
    game_token: UUID = Field(
        default_factory=uuid4,
        index=True,
    )
    main_class: GameClass
    contracts: list[Contract] = Relationship(back_populates="user")
