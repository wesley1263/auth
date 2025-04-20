from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from src.config.config import settings


class MongoDBConfig:
    @staticmethod
    async def get_client() -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.MONGODB_URL)

    @staticmethod
    async def get_database() -> Database:
        client = await MongoDBConfig.get_client()
        return client.auth_service
