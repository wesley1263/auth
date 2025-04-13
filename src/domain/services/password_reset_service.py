from datetime import UTC, datetime, timedelta
from typing import Optional

import jwt
from decouple import config

from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository


class PasswordResetService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.SECRET_KEY = config("SECRET_KEY")
        self.ALGORITHM = "HS256"
        self.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = config("EXPIRES_TOKEN_MINUTES")

    def create_password_reset_token(self, email: str) -> Optional[str]:
        user = self.user_repository.find_by_email(email)
        if not user:
            return None

        expire = datetime.now(UTC.utc) + timedelta(
            minutes=self.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
        )
        token_data = {"sub": email, "exp": expire, "type": "password_reset"}

        return jwt.encode(token_data, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_password_reset_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload.get("type") != "password_reset":
                return None
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except jwt.JWTError:
            return None

    def reset_password(self, token: str, new_password: str) -> bool:
        email = self.verify_password_reset_token(token)
        if not email:
            return False

        user = self.user_repository.find_by_email(email)
        if not user:
            return False

        # Aqui você deve implementar a lógica de hash da senha
        # user.hashed_password = hash_password(new_password)

        # Atualiza o usuário com a nova senha
        updated_user = User(
            **{
                **user.model_dump(),
                "password": new_password,
            }
        )

        return bool(self.user_repository.update(user.id, updated_user.model_dump()))
