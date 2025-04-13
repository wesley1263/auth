from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self):
        # TODO: Mover para variáveis de ambiente
        self.SECRET_KEY = "your-secret-key-here"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.user_repository = UserRepository()

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError:
            return None

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_email(email)
        if not user:
            return None

        # TODO: Implementar verificação de senha
        # if not verify_password(password, user.hashed_password):
        #     return None

        return user
