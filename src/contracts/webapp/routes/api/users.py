from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import select

from contracts.common.db.engine import SessionDep
from contracts.common.enums import GameClass
from contracts.common.models import Contract, User

router = APIRouter(prefix="/api/users", tags=["Users"])


class InUserSchema(BaseModel):
    username: str
    main_class: GameClass


class OutUserSchema(BaseModel):
    identifier: UUID
    username: str
    main_class: str
    contracts: list[Contract]


@router.get("/")
def get_users(session: SessionDep):
    db_users = session.exec(select(User)).all()

    return [
        OutUserSchema(
            identifier=user.identifier,
            username=user.username,
            main_class=user.main_class.name,
            contracts=user.contracts,
        )
        for user in db_users
    ]


@router.post("/")
def create_user(schema: InUserSchema, session: SessionDep) -> OutUserSchema:
    new_user = User(username=schema.username, main_class=schema.main_class)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return OutUserSchema(
        identifier=new_user.identifier,
        username=new_user.username,
        main_class=new_user.main_class.name,
        contracts=[],
    )
