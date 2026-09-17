from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import users_router
from app.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
