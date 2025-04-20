from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import container
from src.domain.dtos.user_dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from src.domain.exceptions import ServiceException
from src.domain.services.user_service import UserService
from src.infrastructure.dependencies import (
    get_auth_service,
    get_oauth_service,
    get_password_reset_service,
)
from src.presentation.dtos.auth_dto import LoginDTO, TokenDTO
from src.presentation.dtos.password_reset_dto import (
    RequestPasswordResetDTO,
    ResetPasswordDTO,
)

router = APIRouter()


@router.post(
    "/auth/login",
    response_model=TokenDTO,
    status_code=200,
    description="Login user",
)
async def login(login_data: LoginDTO, service=Depends(get_auth_service)):
    try:
        return await service.authenticate_user(
            login_data.email,
            login_data.password,
        )
    except ServiceException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message,
        )


@router.post(
    "/auth/google",
    response_model=UserResponseDTO,
    status_code=200,
    description="Login user with google",
)
async def google_auth(token: str, oauth_service=Depends(get_oauth_service)):
    """Login user with google."""
    user = await oauth_service.verify_google_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return user


@router.post(
    "/users",
    response_model=UserResponseDTO,
    status_code=201,
    description="Create user",
)
async def create_user(
    user_data: UserCreateDTO,
    service: UserService = Depends(container.get_user_service),
):
    """Create a new user."""
    try:
        return await service.create_user(user_data)
    except ServiceException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )


@router.get(
    "/users/{user_id}",
    response_model=UserResponseDTO,
    status_code=200,
    description="Get user",
)
async def get_user(
    user_id: str,
    service: UserService = Depends(container.get_user_service),
):
    """Get a user by id."""
    try:
        user = await service.get_user_by_id(user_id)
        return user
    except ServiceException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )


@router.put(
    "/users/{user_id}",
    response_model=UserResponseDTO,
    status_code=200,
    description="Update user",
)
async def update_user(
    user_id: str,
    user_data: UserUpdateDTO,
    service: UserService = Depends(container.get_user_service),
):
    """Update a user."""
    try:
        return await service.update_user(user_id, user_data)
    except ServiceException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )


@router.delete(
    "/users/{user_id}",
    status_code=204,
    description="Delete user",
)
async def delete_user(
    user_id: str,
    service: UserService = Depends(container.get_user_service),
):
    """Delete a user."""
    try:
        await service.delete_user(user_id)
        return {"message": "User deleted successfully"}
    except ServiceException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )


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
