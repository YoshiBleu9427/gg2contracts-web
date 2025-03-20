from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

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
    # TODO server name?
    # TODO creation date
    # TODO last activity date


class User(ContractBaseModel, table=True):
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
    session_token: UUID | None = Field(
        default=None, index=True, unique=True, nullable=True
    )
    server_validated_session: bool = Field(default=False)
    # TODO creation date
    # TODO last activity date


class Contract(ContractBaseModel, table=True):
    identifier: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    contract_type: ContractType
    value: int
    target_value: int
    game_class: GameClass
    completed: bool = Field(default=False)
    points: int

    user_identifier: UUID = Field(default=None, foreign_key="user.identifier")
    user: "User" = Relationship(back_populates="contracts")
    # TODO creation date
    # TODO validate date

    def update_value(self, modifier: int):
        was_completed = self.completed

        self.value += modifier
        self.completed = self.value >= self.target_value

        if self.completed and not was_completed:
            self._on_completion()

    def _on_completion(self):
        self.user.points += self.points
