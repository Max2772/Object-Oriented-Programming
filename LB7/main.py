import uvicorn
from fastapi import FastAPI

from LB7.src.shared.config import settings
from LB7.src.shared.responses import ApiResponse

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=(
        "Finance Tracker API"
    ),
    docs_url="/docs",
    redoc_url="/redoc"
)


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
