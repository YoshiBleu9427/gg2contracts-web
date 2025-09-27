from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from contracts.common.db import queries
from contracts.common.db.engine import SessionDep
from contracts.common.enums import GameClass
from contracts.common.rewards import user_reward_names

router = APIRouter(prefix="/api/users", tags=["Users"])


class InUserSchema(BaseModel):
    username: str
    main_class: GameClass
    reward_names: list[str] | None = None


class OutUserSchema(BaseModel):
    identifier: UUID
    username: str
    main_class: str
    reward_names: list[str]


@router.get("/")
def get_users(session: SessionDep):
    db_users = queries.get_users(session)

    return [
        OutUserSchema(
            identifier=user.identifier,
            username=user.username,
            main_class=user.main_class.name,
            reward_names=user_reward_names(user),
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
        reward_names=user_reward_names(user),
    )


@router.get("/{identifier}/contracts")
def get_user_contracts(session: SessionDep, identifier: str):
    try:
        user_uuid = UUID(identifier)
    except ValueError:
        raise HTTPException(status_code=422, detail="Bad identifier")

    contracts = queries.get_contracts(
        session,
        by__user_identifier=user_uuid,
        order_by__created_at=True,
        order_by__completed=True,
        limit=100,
    )

    return contracts
