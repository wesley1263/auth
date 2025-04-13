from pydantic import BaseModel, EmailStr


class RequestPasswordResetDTO(BaseModel):
    email: EmailStr


class ResetPasswordDTO(BaseModel):
    token: str
    new_password: str
