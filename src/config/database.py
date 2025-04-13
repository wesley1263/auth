from pymongo import MongoClient
from pymongo.database import Database


class MongoDBConfig:
    @staticmethod
    def get_client() -> MongoClient:
        # TODO: Mover para variáveis de ambiente
        MONGO_URI = "mongodb://localhost:27017/auth_db"
        return MongoClient(MONGO_URI)

    @staticmethod
    def get_database() -> Database:
        client = MongoDBConfig.get_client()
        return client.auth_service
