from src.config.config import Settings, settings
from src.domain.services.user_service import UserService
from src.infrastructure.repositories.user_repository import UserRepository


class DependencyInjectionContainer:

    def __init__(self, _settings: Settings):
        """Initialize the container."""
        self.settings = _settings

    def get_user_repository(self) -> UserRepository:
        return UserRepository()

    def get_user_service(self) -> UserService:
        return UserService(self.get_user_repository())


container = DependencyInjectionContainer(settings)
