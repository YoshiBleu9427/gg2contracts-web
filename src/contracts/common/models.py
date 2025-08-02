from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import TIMESTAMP, Field, Relationship, SQLModel

from contracts.common.enums import ContractType, GameClass


class ContractBaseModel(SQLModel):
    pass


class GameServer(ContractBaseModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    validation_token: UUID = Field(
        default_factory=uuid4,
        nullable=False,
    )
    registered_server_name: str
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    last_modified: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
        sa_column_kwargs={"onupdate": lambda: datetime.now()},
    )


class UserRewardLink(ContractBaseModel, table=True):
    user_identifier: UUID | None = Field(
        default=None, foreign_key="user.identifier", primary_key=True
    )
    reward_identifier: UUID | None = Field(
        default=None, foreign_key="reward.identifier", primary_key=True
    )


class Reward(ContractBaseModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    name: str
    description: str
    image_name: str | None
    price: int = Field(default=0)
    users: list["User"] = Relationship(
        back_populates="rewards", link_model=UserRewardLink
    )  # TODO probably dont need that one, study sqlmodel better


class User(ContractBaseModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    username: str
    discord_username: str | None = Field(
        default=None,
        index=True,
        unique=True,
    )
    key_token: UUID = Field(
        default_factory=uuid4,
        index=True,
        unique=True,
    )
    main_class: GameClass
    contracts: list["Contract"] = Relationship(back_populates="user")
    points: int = Field(default=0)

    rewards: list["Reward"] = Relationship(
        back_populates="users", link_model=UserRewardLink
    )

    last_joined_server: UUID | None = Field(
        default=None, foreign_key="gameserver.identifier", nullable=True
    )
    session_token: UUID | None = Field(
        default=None, index=True, unique=True, nullable=True
    )
    server_validated_session: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    last_modified: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
        sa_column_kwargs={"onupdate": lambda: datetime.now()},
    )


class Contract(ContractBaseModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    contract_type: ContractType
    value: int = Field(ge=0)
    target_value: int = Field(ge=0, lt=256)
    game_class: GameClass
    completed: bool = Field(default=False)
    points: int

    user_identifier: UUID = Field(default=None, foreign_key="user.identifier")
    user: "User" = Relationship(back_populates="contracts")

    validated_by_identifier: UUID | None = Field(
        default=None, foreign_key="gameserver.identifier", nullable=True
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
    )
    last_modified: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_type=TIMESTAMP(timezone=True),  # type: ignore
        sa_column_kwargs={"onupdate": lambda: datetime.now()},
    )

    def update_value(self, modifier: int):
        was_completed = self.completed

        self.value += modifier
        self.completed = self.value >= self.target_value

        if self.completed and not was_completed:
            self._on_completion()

    def _on_completion(self):
        self.user.points += self.points
