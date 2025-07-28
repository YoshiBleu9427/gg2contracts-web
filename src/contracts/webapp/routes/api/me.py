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
from contracts.webapp.security import get_current_user, validate_userkey

router = APIRouter(prefix="/api/me", tags=["Users"])

COOKIE_NAME = "userkey"

user_key_cookie = APIKeyCookie(name=COOKIE_NAME, auto_error=False)


class InLoginSchema(BaseModel):
    token: str


class InUserSchema(BaseModel):
    username: str | None
    main_class: GameClass


class OutUserSchema(BaseModel):
    identifier: UUID
    username: str
    main_class: str
    contracts: list[Contract]


@router.get("/")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    time.sleep(0.5)  # totally super secure B)
    if not current_user:
        raise HTTPException(status_code=403)

    return OutUserSchema(
        identifier=current_user.identifier,
        username=current_user.username,
        main_class=current_user.main_class.name,
        contracts=current_user.contracts,
    )


@router.post("/login")
def login(schema: InLoginSchema, session: SessionDep) -> JSONResponse:
    time.sleep(1)  # totally super secure B)

    current_user = validate_userkey(session, user_key=schema.token)
    if not current_user:
        raise HTTPException(status_code=403)

    session.commit()

    response = JSONResponse(None)

    response.set_cookie(
        COOKIE_NAME,
        value=current_user.key_token.hex,
        max_age=3 * 60 * 60 * 1000,
    )

    return response


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

    session.commit()

    return OutUserSchema(
        identifier=current_user.identifier,
        username=current_user.username,
        main_class=current_user.main_class.name,
        contracts=[],
    )
