import bcrypt

from src.domain.dtos.user_dto import (
    UserCreateDTO,
    UserDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from src.domain.exceptions import ServiceException
from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def _validate_user_exists(self, user: User):
        user = await self.user_repository.find_by_email(user.email)
        if user:
            raise ServiceException(f"User with email {user.email} already exists", 400)

    async def create_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        user = User(**user_data.model_dump())
        await self._validate_user_exists(user)
        user.password = await self._generate_password_hash(user.password)
        result = await self.user_repository.create(user)
        return UserResponseDTO(**result.model_dump())

    async def get_user_by_id(self, user_id) -> UserResponseDTO:
        result = await self.user_repository.find_by_id(user_id)
        if not result:
            raise ServiceException(f"User with id {user_id} not found", 404)
        return UserResponseDTO(**result.model_dump())

    async def get_user_by_email(self, email) -> UserDTO | None:
        result = await self.user_repository.find_by_email(email)
        if not result:
            raise ServiceException(f"User with email {email} not found", 404)
        return UserDTO(**result.model_dump())

    async def update_user(
        self,
        user_id: str,
        payload: UserUpdateDTO,
    ) -> UserResponseDTO | None:
        """Update a user."""
        result = await self.get_user_by_id(user_id)
        user_data = result.model_dump()
        payload.password = await self._generate_password_hash(payload.password)
        user_data.update(payload.model_dump())
        user_data.pop("id")
        result = await self.user_repository.update(
            user_id,
            user_data,
        )
        if not result:
            return None
        return UserResponseDTO(**result.model_dump())

    async def delete_user(self, user_id):
        return await self.user_repository.delete(user_id)

    async def _generate_password_hash(self, password: str) -> str:
        """Generate a password hash."""
        result = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return result.decode("utf-8")

    async def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password."""
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
