from datetime import UTC, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True
    password: str
    external_id: Optional[str] = None
    created_at: datetime = datetime.now(UTC.utc)
    updated_at: datetime = datetime.now(UTC.utc)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "external_id": "google_12345",
            }
        }
