from datetime import UTC, datetime, timedelta
from typing import Optional

from jose import jwt
from loguru import logger

from src.config.config import settings
from src.domain.exceptions import ServiceException
from src.domain.services.user_service import UserService
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.dtos.auth_dto import TokenDTO


class AuthService:
    def __init__(self, user_repository: UserRepository, user_service: UserService):
        self._repo = user_repository
        self._user_service = user_service

    async def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(UTC.utc) + expires_delta
        else:
            expire = datetime.now(UTC.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except jwt.JWTError as err:
            logger.error(f"Error decoding token: {err}")
            return None

    async def authenticate_user(self, email: str, password: str) -> TokenDTO:
        user = await self._user_service.get_user_by_email(email)
        if not await self._user_service._verify_password(
            password,
            user.password,
        ):
            raise ServiceException("Invalid credentials", 401)
        access_token = await self.create_access_token({"sub": user.id})
        return TokenDTO(access_token=access_token)
