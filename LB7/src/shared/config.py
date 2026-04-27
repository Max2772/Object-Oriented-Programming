from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Finance Tracker API"
    APP_VERSION: str = "1.0.0"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    RELOAD: bool = True

    DATABASE_URL: str = "sqlite:///finance_tracker.db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
