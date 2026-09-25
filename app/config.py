# app/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/stockdb"

    # Auth / Session
    SECRET_KEY: str = "change-this-secret-key"
    SESSION_COOKIE_NAME: str = "stock_app_session"

    # CORS - frontend origins allowed to call this API
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()