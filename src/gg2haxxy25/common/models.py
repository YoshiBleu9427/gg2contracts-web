from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from gg2haxxy25.common.enums import ContractType, GameClass


class GameServer(SQLModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )


class User(SQLModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username: str
    key_token: UUID = Field(
        default_factory=uuid4,
        index=True,
        unique=True,
    )
    main_class: GameClass
    contracts: list["Contract"] = Relationship(back_populates="user")
    points: int = Field(default=0)

    last_joined_server: UUID | None = Field(
        default=None, foreign_key="gameserver.identifier", nullable=True
    )
    challenge_token: UUID | None = Field(
        default=None, index=True, unique=True, nullable=True
    )
    server_validated_challenge: bool = Field(default=False)


class Contract(SQLModel, table=True):
    identifier: UUID = Field(default=None, primary_key=True)
    contract_type: ContractType
    value: int
    target_value: int
    game_class: GameClass
    completed: bool = Field(default=False)
    points: int

    user_identifier: UUID = Field(default=None, foreign_key="user.identifier")
    user: "User" = Relationship(back_populates="contracts")
