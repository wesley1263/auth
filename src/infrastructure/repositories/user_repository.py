import asyncio
from typing import Optional

from bson import ObjectId
from loguru import logger
from pymongo.errors import PyMongoError

from src.config.database import MongoDBConfig
from src.domain.models.user import User


class UserRepository:
    def __init__(self):
        self.db = asyncio.run(MongoDBConfig.get_database())
        self.collection = self.db.users

    async def create(self, user: User) -> User | None:
        try:
            user_dict = user.model_dump(exclude={"id"})
            result = await self.collection.insert_one(user_dict)
            user.id = str(result.inserted_id)
            return user
        except PyMongoError as e:
            logger.error(f"Error creating user: {e}")
            return None

    async def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_data = await self.collection.find_one({"_id": ObjectId(user_id)})
            if user_data:
                user_data["id"] = str(user_data.pop("_id"))
                return User(**user_data)
            return None
        except PyMongoError as e:
            logger.error(f"Error finding user by ID: {e}")
            return None

    async def find_by_email(self, email: str) -> Optional[User]:
        user_data = await self.collection.find_one({"email": email})
        if user_data:
            user_data["id"] = str(user_data.pop("_id"))
            return User(**user_data)
        return None

    async def find_by_external_id(self, external_id: str) -> Optional[User]:
        user_data = await self.collection.find_one({"external_id": external_id})
        if user_data:
            user_data["id"] = str(user_data.pop("_id"))
            return User(**user_data)
        return None

    async def update(self, user_id: str, user_data: dict) -> Optional[User]:
        try:
            result = await self.collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": user_data}
            )
            if result.modified_count:
                return await self.find_by_id(user_id)
            return None
        except PyMongoError as e:
            logger.error(f"Error updating user: {e}")
            return None

    async def delete(self, user_id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except PyMongoError as e:
            logger.error(f"Error deleting user: {e}")
            return False
