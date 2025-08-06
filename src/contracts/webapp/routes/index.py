from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlmodel import select

from contracts.common.db.engine import SessionDep
from contracts.common.models import User
from contracts.common.rewards import ALL_REWARDS, user_reward_names
from contracts.webapp.security import get_current_user
from contracts.webapp.settings import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("pages/index.html", context)
    return response


@router.get("/users", response_class=HTMLResponse)
def users_page(request: Request, session: SessionDep):
    db_users = session.exec(select(User)).all()
    context = {"request": request, "users": db_users}
    response = templates.TemplateResponse("pages/users.html", context)
    return response


@router.get("/me", response_class=HTMLResponse)
def me_page(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user:
        context = {
            "request": request,
            "user": current_user,
            "rewards": user_reward_names(current_user),
            "all_rewards": ALL_REWARDS,
        }
        response = templates.TemplateResponse("pages/updateme.html", context)
    else:
        context = {"request": request}
        response = templates.TemplateResponse("pages/loginme.html", context)
    return response
