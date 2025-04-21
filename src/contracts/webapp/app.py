from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contracts.common.db.engine import on_startup
from contracts.common.logging import logger
from contracts.webapp.routes import index
from contracts.webapp.routes.api import users
from contracts.webapp.settings import BASE_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup database before starting the app
    logger.info("Setting up database...")
    on_startup()
    logger.info("Done.")
    yield


app = FastAPI(
    title="The gg2 contracts website",
    description="Gang Garrison 2 Contracts Website and Backend",
    version="0.1.2",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(index.router)
app.include_router(users.router)
