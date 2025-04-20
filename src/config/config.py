from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("EXPIRES_TOKEN_MINUTES", cast=int)
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")
    MONGODB_URL: str = config("MONGODB_URL")


settings = Settings()
