from pydantic import BaseModel, EmailStr


class RequestPasswordResetDTO(BaseModel):
    email: EmailStr


class OTPRequestPasswordResetDTO(BaseModel):
    code: str
    email: str


class OTPResetPasswordDTO(BaseModel):
    code: str
    password: str
    email: str
