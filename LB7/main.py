from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from LB7.src.api.account_handlers import ACCOUNT_ROUTER
from LB7.src.api.auth_handlers import AUTH_ROUTER
from LB7.src.clients.database import init_db
from LB7.src.shared.config import settings
from LB7.src.shared.responses import ApiResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=(
        "Finance Tracker API"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

API_PREFIX = "/api/v1"

app.include_router(ACCOUNT_ROUTER, prefix=API_PREFIX)
app.include_router(AUTH_ROUTER, prefix=API_PREFIX)


@app.get("/", tags=["General"], summary="Base endpoint")
def root():
    return ApiResponse(
        data=settings.APP_TITLE,
        message=settings.APP_VERSION
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.RELOAD,
    )
