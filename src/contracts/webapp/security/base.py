from typing import Annotated

from fastapi import Depends, Request

from contracts.common.db import queries
from contracts.common.db.engine import SessionDep
from contracts.common.logging import logger
from contracts.common.models import User

from .cookie import get_cookie_user
from .oauth import get_discord_username, is_trying_to_login_with_discord


async def get_current_user(
    session: SessionDep,
    request: Request,
    cookie_user: Annotated[User | None, Depends(get_cookie_user)],
) -> User | None:
    if is_trying_to_login_with_discord(request):
        logger.debug("get_current_user is_trying_to_login_with_discord")
        oauth_code = request.query_params.get("code")
        if oauth_code:
            discord_username = await get_discord_username(oauth_code)
            if discord_username:
                if cookie_user:
                    cookie_user.discord_username = discord_username
                    logger.debug(
                        f"get_current_user linking user {cookie_user.username} to discord {discord_username}"
                    )
                    session.commit()
                    return cookie_user
                else:
                    discord_user = queries.get_user(
                        session, by__discord_username=discord_username
                    )
                    logger.debug(
                        f"get_current_user fetched discord_user {discord_user.username if discord_user else None}"
                    )
                    if discord_user:
                        return discord_user

    logger.debug(
        f"get_current_user default cookieuser {cookie_user.username if cookie_user else None}"
    )
    return cookie_user
