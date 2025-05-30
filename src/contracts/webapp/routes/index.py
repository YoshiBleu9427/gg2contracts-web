from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlmodel import select

from contracts.common.db.engine import SessionDep
from contracts.common.models import User
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
def me_page(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("pages/updateme.html", context)
    return response
