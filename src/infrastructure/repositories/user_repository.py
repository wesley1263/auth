from typing import Optional

from bson import ObjectId

from src.config.database import MongoDBConfig
from src.domain.models.user import User


class UserRepository:
    def __init__(self):
        self.db = MongoDBConfig.get_database()
        self.collection = self.db.users

    def create(self, user: User) -> User:
        user_dict = user.model_dump(exclude={"id"})
        result = self.collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_data = self.collection.find_one({"_id": ObjectId(user_id)})
            if user_data:
                user_data["id"] = str(user_data.pop("_id"))
                return User(**user_data)
            return None
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None

    def find_by_email(self, email: str) -> Optional[User]:
        user_data = self.collection.find_one({"email": email})
        if user_data:
            user_data["id"] = str(user_data.pop("_id"))
            return User(**user_data)
        return None

    def find_by_external_id(self, external_id: str) -> Optional[User]:
        user_data = self.collection.find_one({"external_id": external_id})
        if user_data:
            user_data["id"] = str(user_data.pop("_id"))
            return User(**user_data)
        return None

    def update(self, user_id: str, user_data: dict) -> Optional[User]:
        result = self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": user_data}
        )
        if result.modified_count:
            return self.find_by_id(user_id)
        return None

    def delete(self, user_id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
