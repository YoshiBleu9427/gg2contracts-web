import time
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, event
from sqlmodel import Session, SQLModel, create_engine

from contracts.common.logging import logger
from contracts.common.settings import settings

connect_args = {"check_same_thread": False}
engine = create_engine(settings.db_uri, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


if settings.debug:

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.debug("Start Query: %s" % statement)

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f" % total)


SessionDep = Annotated[Session, Depends(get_session)]


def on_startup():
    create_db_and_tables()
