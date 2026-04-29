from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )
    APP_TITLE: str = "Finance Tracker API"
    APP_VERSION: str = "1.0.0"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    RELOAD: bool = True

    SECRET_KEY: str = "1234"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite:///./finance_tracker.db"


settings = Settings()
