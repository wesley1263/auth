from typing import Optional

from google.auth.transport import requests
from google.oauth2 import id_token

from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository


class OAuthService:
    def __init__(self):
        # TODO: Mover para variáveis de ambiente
        self.GOOGLE_CLIENT_ID = "your-google-client-id"
        self.user_repository = UserRepository()

    async def verify_google_token(self, token: str) -> Optional[User]:
        try:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.GOOGLE_CLIENT_ID
            )

            if idinfo["iss"] not in [
                "accounts.google.com",
                "https://accounts.google.com",
            ]:
                raise ValueError("Invalid Token")

            user_data = {
                "email": idinfo["email"],
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
                "external_id": f"google_{idinfo['sub']}",
            }

            # Verifica se o usuário já existe
            existing_user = self.user_repository.find_by_email(user_data["email"])
            if existing_user:
                return existing_user

            new_user = User(**user_data)
            return self.user_repository.create(new_user)

        except ValueError:
            return None
