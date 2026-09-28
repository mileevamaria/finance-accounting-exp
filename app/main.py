from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import (
    accounts,
    auth,
    categories,
    companies,
    projects,
    reports,
    subscriptions,
    transactions,
    users,
    websockets,
)
from app.db import engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# REST API
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(companies.router)
app.include_router(accounts.router)
app.include_router(categories.router)
app.include_router(projects.router)
app.include_router(transactions.router)
app.include_router(reports.router)
app.include_router(subscriptions.router)

# WebSocket
app.include_router(websockets.router)
