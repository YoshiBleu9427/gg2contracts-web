from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from contracts.common.models import User
from contracts.common.rewards import ALL_REWARDS, user_reward_names
from contracts.webapp.security.base import get_current_user
from contracts.webapp.security.cookie import set_cookie, unset_cookie
from contracts.webapp.security.oauth import (
    get_oauth_login_url,
    is_oauth_enabled,
    is_trying_to_login_with_discord,
)
from contracts.webapp.settings import templates

router = APIRouter(prefix="/me")


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def me_page(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    tried_to_login_with_discord: Annotated[
        bool, Depends(is_trying_to_login_with_discord)
    ],
):
    discord_oauth_login_url = get_oauth_login_url() if is_oauth_enabled() else ""
    if current_user:
        if is_oauth_enabled() and tried_to_login_with_discord:
            response = RedirectResponse("/me/")
            set_cookie(current_user, response)
            return response
        else:
            context = {
                "request": request,
                "user": current_user,
                "discord_oauth_login_url": discord_oauth_login_url,
                "rewards": user_reward_names(current_user),
                "all_rewards": ALL_REWARDS,
            }
            return templates.TemplateResponse("pages/updateme.html", context)
    else:
        context = {
            "request": request,
            "discord_oauth_login_url": discord_oauth_login_url,
            "tried_to_login_with_discord": tried_to_login_with_discord,
        }
        return templates.TemplateResponse("pages/loginme.html", context)


@router.get("/logout", response_class=HTMLResponse)
def logout_page():
    resp = RedirectResponse("/me/")
    unset_cookie(resp)
    return resp
