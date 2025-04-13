from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str


settings = Settings()
