from typing import Optional

from jose import jwt
import pyotp

from src.config.config import settings
from src.domain.exceptions import ServiceException
from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository
from src.presentation.dtos.password_reset_dto import OTPRequestPasswordResetDTO, OTPResetPasswordDTO


class PasswordResetService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def reset_password_otp_code(self, email: str) -> OTPRequestPasswordResetDTO:
        user = await self.user_repository.find_by_email(email)
        if not user:
            raise ServiceException("User not found", 404)
        totp = pyotp.TOTP(settings.OTP_SECRET, interval=60)
        # TODO: Implement the email sending
        return OTPRequestPasswordResetDTO(
            code=totp.now(),
            email=email,
        )

    async def verify_otp_password_reset(self, payload: OTPResetPasswordDTO) -> bool:
        user = await self.user_repository.find_by_email(
            payload.email,
        )
        if not user:
            raise ServiceException("User not found", 404)
        totp = pyotp.TOTP(settings.OTP_SECRET)
        if not totp.verify(payload.code):
            raise ServiceException("Invalid code", 400)
        return True

    async def verify_password_reset_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
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
