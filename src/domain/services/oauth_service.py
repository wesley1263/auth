from google.auth.transport import requests
from google.oauth2 import id_token

from src.config.config import settings
from src.domain.dtos.user_dto import UserCreateDTO, UserResponseDTO
from src.domain.exceptions import ServiceException
from src.domain.services.user_service import UserService


class OAuthService:
    def __init__(
        self,
        user_service: UserService,
    ):
        self.user_service = user_service

    async def verify_google_token(self, token: str) -> UserResponseDTO:
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            if id_info["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ServiceException("Invalid Token", 401)

            user_data = UserCreateDTO(
                email=id_info["email"],
                first_name=id_info.get("given_name", ""),
                last_name=id_info.get("family_name", ""),
                external_id=f"google_{id_info['sub']}",
            )
            return await self.user_service.create_user(user_data)
        except ValueError:
            raise ServiceException("Invalid Token", 401)
