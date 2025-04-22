from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    external_id: Optional[str] = None


class UserDTO(UserCreateDTO):
    id: str
    is_active: bool


class UserResponseDTO(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    external_id: Optional[str] = None
    is_active: bool


class UserUpdateDTO(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    external_id: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
