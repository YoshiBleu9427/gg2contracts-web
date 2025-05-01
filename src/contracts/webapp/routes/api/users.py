import time
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from contracts.common.db import queries
from contracts.common.db.engine import SessionDep
from contracts.common.enums import GameClass
from contracts.common.models import Contract, User

router = APIRouter(prefix="/api/users", tags=["Users"])


class InUserSchema(BaseModel):
    username: str
    main_class: GameClass
    discord_username: str | None


class OutUserSchema(BaseModel):
    identifier: UUID
    username: str
    main_class: str
    contracts: list[Contract]


def _raise_if_discord_username_exists(session: SessionDep, discord_username: str):
    if queries.get_user(session, by__discord_username=discord_username):
        raise HTTPException(
            status_code=422,
            detail="A different user already claimed this discord username.",
        )


@router.get("/")
def get_users(session: SessionDep):
    db_users = queries.get_users(session)

    return [
        OutUserSchema(
            identifier=user.identifier,
            username=user.username,
            main_class=user.main_class.name,
            contracts=user.contracts,
        )
        for user in db_users
    ]


@router.get("/{identifier}")
def get_user(session: SessionDep, identifier: str):
    try:
        user_uuid = UUID(identifier)
    except ValueError:
        raise HTTPException(status_code=422, detail="Bad identifier")

    user = queries.get_user(session, by__identifier=user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return OutUserSchema(
        identifier=user.identifier,
        username=user.username,
        main_class=user.main_class.name,
        contracts=user.contracts,
    )


@router.post("/")
def create_user(schema: InUserSchema, session: SessionDep) -> OutUserSchema:
    time.sleep(1)  # totally super secure B)

    if schema.discord_username:
        _raise_if_discord_username_exists(session, schema.discord_username)

    new_user = User(
        username=schema.username,
        main_class=schema.main_class,
        discord_username=schema.discord_username,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return OutUserSchema(
        identifier=new_user.identifier,
        username=new_user.username,
        main_class=new_user.main_class.name,
        contracts=[],
    )


@router.put("/{user_key}")
def update_user(
    schema: InUserSchema, user_key: str, session: SessionDep
) -> OutUserSchema:
    time.sleep(1)  # totally super secure B)

    try:
        UUID(user_key)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")

    found_user = queries.get_user(session, by__key_token=UUID(user_key))
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")

    found_user.username = schema.username
    found_user.main_class = schema.main_class

    if schema.discord_username:
        _raise_if_discord_username_exists(session, schema.discord_username)
        found_user.discord_username = schema.discord_username

    session.commit()

    return OutUserSchema(
        identifier=found_user.identifier,
        username=found_user.username,
        main_class=found_user.main_class.name,
        contracts=[],
    )
