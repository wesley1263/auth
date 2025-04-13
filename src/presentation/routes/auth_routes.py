from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from src.domain.dtos.user_dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from src.domain.models.user import User
from src.infrastructure.dependencies import (
    get_auth_service,
    get_oauth_service,
    get_password_reset_service,
    get_user_repository,
)
from src.presentation.dtos.auth_dto import LoginDTO, TokenDTO
from src.presentation.dtos.password_reset_dto import (
    RequestPasswordResetDTO,
    ResetPasswordDTO,
)

router = APIRouter()


@router.post(
    "/auth/login", response_model=TokenDTO, status_code=200, description="Login user"
)
async def login(login_data: LoginDTO, auth_service=Depends(get_auth_service)):
    user = auth_service.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    access_token = auth_service.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return TokenDTO(access_token=access_token)


@router.post(
    "/auth/google",
    response_model=UserResponseDTO,
    status_code=200,
    description="Login user with google",
)
async def google_auth(token: str, oauth_service=Depends(get_oauth_service)):
    user = await oauth_service.verify_google_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return user


@router.post(
    "/users", response_model=UserResponseDTO, status_code=201, description="Create user"
)
async def create_user(
    user_data: UserCreateDTO, user_repository=Depends(get_user_repository)
):
    existing_user = user_repository.find_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail already registered")

    user = User(**user_data.model_dump())
    created_user = user_repository.create(user)
    return created_user


@router.get(
    "/users/{user_id}",
    response_model=UserResponseDTO,
    status_code=200,
    description="Get user",
)
async def get_user(user_id: str, user_repository=Depends(get_user_repository)):
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.put(
    "/users/{user_id}",
    response_model=UserResponseDTO,
    status_code=200,
    description="Update user",
)
async def update_user(
    user_id: str, user_data: UserUpdateDTO, user_repository=Depends(get_user_repository)
):
    updated_user = user_repository.update(
        user_id, user_data.model_dump(exclude_unset=True)
    )
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return updated_user


@router.delete("/users/{user_id}", status_code=204, description="Delete user")
async def delete_user(user_id: str, user_repository=Depends(get_user_repository)):
    if not user_repository.delete(user_id):
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return {"message": "User deleted successfully"}


@router.post(
    "/auth/forgot-password", status_code=200, description="Request password reset"
)
async def request_password_reset(
    request_data: RequestPasswordResetDTO,
    password_reset_service=Depends(get_password_reset_service),
):
    token = password_reset_service.create_password_reset_token(request_data.email)
    if not token:
        raise HTTPException(status_code=404, detail="Email não encontrado")

    # TODO: Implementar o envio do email com o token
    # Por enquanto, retornamos o token diretamente para fins de teste
    return {"message": "Token de redefinição enviado", "token": token}


@router.post("/auth/reset-password", status_code=200, description="Reset password")
async def reset_password(
    reset_data: ResetPasswordDTO,
    password_reset_service=Depends(get_password_reset_service),
):
    if not password_reset_service.reset_password(
        reset_data.token, reset_data.new_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Token has expired or invalid",
        )
    return {"message": "Password reset successfully"}
