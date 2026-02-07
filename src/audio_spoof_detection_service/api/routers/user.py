from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from audio_spoof_detection_service.api.auth import get_current_user
from audio_spoof_detection_service.api.schemas.user import (
    RegisterUserRequest, RegisterUserResponse, LoginUserRequest, LoginUserResponse, LogoutUserRequest,
    LogoutUserResponse, RefreshTokensRequest, RefreshTokensResponse, GetUserInfoResponse
)
from audio_spoof_detection_service.api.schemas.error import ErrorResponse
from audio_spoof_detection_service.application.contracts.user import (
    RegisterUserInputDTO, LoginUserInputDTO, LogoutUserInputDTO, GetUserInfoOutputDTO,
    RefreshUserTokensInputDTO
)
from audio_spoof_detection_service.application.usecases.user import (
    RegisterUserUseCase, LoginUserUseCase, LogoutUserUseCase, RefreshUserTokensUseCase
)


user_router = APIRouter(route_class=DishkaRoute, prefix='/user', tags=['User'])


@user_router.post(
    path='/register',
    responses={
        200: {'model': RegisterUserResponse},
        404: {'model': ErrorResponse}
    }
)
async def register(
        request: RegisterUserRequest,
        register_user_interactor: FromDishka[RegisterUserUseCase],
) -> JSONResponse:
    output_dto = await register_user_interactor(
        RegisterUserInputDTO(username=request.username, email=str(request.email), password=request.password)
    )
    response = RegisterUserResponse(
        username=output_dto.user.name, email=output_dto.user.email, registered_at=output_dto.user.registered_at
    )
    return JSONResponse(response.model_dump(mode='json'))


@user_router.post(
    path='/login',
    responses={
        200: {'model': LoginUserResponse},
        404: {'model': ErrorResponse}
    }
)
async def login(
        request: LoginUserRequest,
        login_user_interactor: FromDishka[LoginUserUseCase]
) -> JSONResponse:
    output = await login_user_interactor(
        LoginUserInputDTO(email=str(request.email), password=request.password)
    )
    response = LoginUserResponse(access_token=output.access_token, refresh_token=output.refresh_token)
    return JSONResponse(response.model_dump(mode='json'))


@user_router.post(
    path='/logout',
    responses={
        200: {'model': LogoutUserResponse},
        404: {'model': ErrorResponse}
    }
)
async def logout(
        request: LogoutUserRequest,
        logout_user_interactor: FromDishka[LogoutUserUseCase]
) -> JSONResponse:
    await logout_user_interactor(LogoutUserInputDTO(refresh_token=request.refresh_token))
    response = LogoutUserResponse(message='Выход из аккаунта выполнен успешно.')
    return JSONResponse(response.model_dump(mode='json'))


@user_router.post(
    path='/refresh_tokens',
    responses={
        200: {'model': RefreshTokensResponse},
        404: {'model': ErrorResponse}
    }
)
async def refresh_tokens(
        request: RefreshTokensRequest,
        refresh_user_tokens_interactor: FromDishka[RefreshUserTokensUseCase]
) -> JSONResponse:
    token_pair = await refresh_user_tokens_interactor(RefreshUserTokensInputDTO(refresh_token=request.refresh_token))
    response = RefreshTokensResponse(access_token=token_pair.access_token, refresh_token=token_pair.refresh_token)
    return JSONResponse(response.model_dump(mode='json'))


@user_router.get(
    path='/me',
    responses={
        200: {'model': GetUserInfoResponse},
        404: {'model': ErrorResponse}
    }
)
async def me(get_user_info_interactor_result: GetUserInfoOutputDTO = Depends(get_current_user)) -> JSONResponse:
    current_user = get_user_info_interactor_result.user
    response = GetUserInfoResponse(
        user_id=current_user.id,
        username=current_user.name,
        email=current_user.email,
        registered_at=current_user.registered_at
    )
    return JSONResponse(response.model_dump(mode='json'))
