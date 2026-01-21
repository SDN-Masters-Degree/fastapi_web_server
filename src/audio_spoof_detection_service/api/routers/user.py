from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from audio_spoof_detection_service.api.schemas.user import (
    RegisterUserRequest, RegisterUserResponse,
    LoginUserRequest, LoginUserResponse
)
from audio_spoof_detection_service.api.schemas.error import ErrorResponse
from audio_spoof_detection_service.application.contracts.user import (
    RegisterUserInputDTO, LoginUserInputDTO
)
from audio_spoof_detection_service.application.usecases.user import (
    RegisterUserUseCase, LoginUserUseCase
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
        register_user_interactor: FromDishka[RegisterUserUseCase]
) -> JSONResponse:
    output_dto = await register_user_interactor(RegisterUserInputDTO(request.username, str(request.email)))
    response = RegisterUserResponse(
        username=output_dto.result.name,
        email=output_dto.result.email,
        registered_at=output_dto.result.registered_at
    )
    return JSONResponse(response.model_dump())


@user_router.post(
    path='/request_otp'
)
async def request_otp() -> JSONResponse:
    pass


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
        LoginUserInputDTO(email=str(request.email), one_time_password=request.one_time_password)
    )
    response = LoginUserResponse(access_token=output.result.access_token, refresh_token=output.result.access_token)
    return JSONResponse(response.model_dump())


@user_router.post(
    path='/logout'
)
async def logout() -> JSONResponse:
    # просто стереть токен из записи юзера и все
    pass


@user_router.post(
    path='/refresh_token'
)
async def refresh_token() -> JSONResponse:
    pass
