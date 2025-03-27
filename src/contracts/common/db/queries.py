from typing import Sequence
from uuid import UUID

from sqlmodel import Session, select

from contracts.common.models import Contract, GameServer, User


def get_users(
    session: Session,
    by__server_id: UUID | None = None,
    by__server_validated: bool | None = None,
) -> Sequence[User]:
    query = select(User)

    if by__server_id:
        query = query.where(User.last_joined_server == by__server_id)

    if by__server_validated is not None:
        query = query.where(User.server_validated_session == by__server_validated)

    return session.exec(query).all()


def get_user(
    session: Session,
    by__identifier: UUID | None = None,
    by__key_token: UUID | None = None,
    by__session_token: UUID | None = None,
    by__username: str | None = None,
) -> User | None:
    query = select(User)

    if by__identifier:
        query = query.where(User.identifier == by__identifier)

    if by__key_token:
        query = query.where(User.key_token == by__key_token)

    if by__session_token:
        query = query.where(User.session_token == by__session_token)

    if by__username:
        query = query.where(User.username == by__username)

    return session.exec(query).one_or_none()


def get_game_server(
    session: Session,
    by__identifier: UUID | None = None,
) -> GameServer | None:
    query = select(GameServer)

    if by__identifier:
        query = query.where(GameServer.identifier == by__identifier)

    return session.exec(query).one_or_none()


def get_contract(
    session: Session,
    by__identifier: UUID | None = None,
) -> Contract | None:
    query = select(Contract)

    if by__identifier:
        query = query.where(Contract.identifier == by__identifier)

    return session.exec(query).one_or_none()


def get_contracts(
    session: Session,
    by__user_identifier: UUID | None = None,
    by__completed: bool | None = None,
) -> Sequence[Contract]:
    query = select(Contract)

    if by__user_identifier:
        query = query.where(Contract.user_identifier == by__user_identifier)

    if by__completed is not None:
        query = query.where(Contract.completed == by__completed)

    return session.exec(query).all()
