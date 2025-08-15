from typing import Annotated
from uuid import UUID

from fastapi import Depends, Response
from fastapi.security import APIKeyCookie
from pydantic import BaseModel

from contracts.common.db import queries
from contracts.common.db.engine import SessionDep
from contracts.common.models import User

COOKIE_NAME = "userkey"

user_key_cookie = APIKeyCookie(name=COOKIE_NAME, auto_error=False)


class InLoginSchema(BaseModel):
    token: str


def validate_userkey(session: SessionDep, user_key: str | None) -> User | None:
    if not user_key:
        return None

    try:
        return queries.get_user(session, by__key_token=UUID(user_key))
    except ValueError:
        return None


def set_cookie(user: User, response: Response):
    response.set_cookie(
        COOKIE_NAME,
        value=user.key_token.hex,
        max_age=24 * 60 * 60,
    )


def unset_cookie(response: Response):
    response.delete_cookie(COOKIE_NAME)


async def get_cookie_user(
    session: SessionDep, user_key: Annotated[str | None, Depends(user_key_cookie)]
) -> User | None:
    return validate_userkey(session, user_key)
