from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from contracts.common.db.engine import SessionDep
from contracts.common.db.queries import get_users
from contracts.webapp.settings import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    context = {"request": request}
    response = templates.TemplateResponse("pages/index.html", context)
    return response


@router.get("/users", response_class=HTMLResponse)
def users_page(request: Request, session: SessionDep):
    db_users = get_users(session, order_by__points=True)
    context = {"request": request, "users": db_users}
    response = templates.TemplateResponse("pages/users.html", context)
    return response
