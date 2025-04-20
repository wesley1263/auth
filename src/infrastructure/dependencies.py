from src.domain.services.auth_service import AuthService
from src.domain.services.oauth_service import OAuthService
from src.domain.services.password_reset_service import PasswordResetService
from src.domain.services.user_service import UserService
from src.infrastructure.repositories.user_repository import UserRepository
# TODO: Move all to core/dependencies.py

def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service() -> UserService:
    return UserService(get_user_repository())


def get_oauth_service() -> OAuthService:
    user_repository = get_user_repository()
    return OAuthService(user_repository=user_repository)


def get_auth_service() -> AuthService:
    return AuthService(
        get_user_repository(),
        get_user_service(),
    )


def get_password_reset_service() -> PasswordResetService:
    return PasswordResetService(get_user_repository())
