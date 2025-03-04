from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlmodel import select

from gg2haxxy25.common.db.engine import SessionDep
from gg2haxxy25.common.models.user import User
from gg2haxxy25.webapp.settings import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    context = {"request": request, "extra_text": "Injected value"}
    response = templates.TemplateResponse("index.html", context)
    return response


@router.get("/users", response_class=HTMLResponse)
def users_page(request: Request, session: SessionDep):
    db_users = session.exec(select(User)).all()
    context = {"request": request, "users": db_users}
    response = templates.TemplateResponse("users.html", context)
    return response
