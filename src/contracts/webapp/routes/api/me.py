import time
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie
from pydantic import BaseModel

from contracts.common.db.engine import SessionDep
from contracts.common.enums import GameClass
from contracts.common.models import Contract, User
from contracts.common.rewards import (
    InsufficientFunds,
    TooManyMedals,
    grant_from_names,
    user_reward_names,
)
from contracts.webapp.security.base import get_current_user
from contracts.webapp.security.cookie import set_cookie, validate_userkey

router = APIRouter(prefix="/api/me", tags=["Users"])

COOKIE_NAME = "userkey"

user_key_cookie = APIKeyCookie(name=COOKIE_NAME, auto_error=False)


class InLoginSchema(BaseModel):
    token: str


class InUserSchema(BaseModel):
    username: str | None = None
    main_class: GameClass
    reward_names: list[str] | None = None


class OutUserSchema(BaseModel):
    identifier: UUID
    username: str
    main_class: str
    contracts: list[Contract]
    reward_names: list[str]


@router.get("")
@router.get("/")
async def get_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    time.sleep(0.5)  # totally super secure B)
    if not current_user:
        raise HTTPException(status_code=403)

    return OutUserSchema(
        identifier=current_user.identifier,
        username=current_user.username,
        main_class=current_user.main_class.name,
        contracts=current_user.contracts,
        reward_names=user_reward_names(current_user),
    )


@router.post("/login")
def login(schema: InLoginSchema, session: SessionDep) -> JSONResponse:
    time.sleep(1)  # totally super secure B)

    current_user = validate_userkey(session, user_key=schema.token)
    if not current_user:
        raise HTTPException(status_code=403)

    resp = JSONResponse(None)
    set_cookie(current_user, resp)
    return resp


@router.put("")
@router.put("/")
def update_user(
    schema: InUserSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
) -> OutUserSchema:
    time.sleep(0.5)  # totally super secure B)
    if schema.username:
        current_user.username = schema.username

    current_user.main_class = schema.main_class

    if schema.reward_names:
        try:
            grant_from_names(current_user, schema.reward_names)
        except TooManyMedals:
            raise HTTPException(status_code=422, detail="Too many medals selected")
        except InsufficientFunds:
            raise HTTPException(status_code=422, detail="Rewards too expensive")

    session.commit()

    return OutUserSchema(
        identifier=current_user.identifier,
        username=current_user.username,
        main_class=current_user.main_class.name,
        contracts=[],
        reward_names=user_reward_names(current_user),
    )
