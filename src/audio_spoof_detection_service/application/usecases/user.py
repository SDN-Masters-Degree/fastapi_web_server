from datetime import datetime

from audio_spoof_detection_service.application.common.interactor import Interactor
from audio_spoof_detection_service.application.protocols.database_gateways.user_gateway import UserGateway
from audio_spoof_detection_service.application.protocols.providers.token_provider import TokenProvider
from audio_spoof_detection_service.application.contracts.user import (
    GetUserInfoInputDTO, GetUserInfoOutputDTO,
    RegisterUserInputDTO, RegisterUserOutputDTO,
    LoginUserInputDTO, LoginUserOutputDTO
)
from audio_spoof_detection_service.infrastructure.settings import Settings
from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.error import UserError


class GetUserInfoUseCase(Interactor[GetUserInfoInputDTO, GetUserInfoOutputDTO]):
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: GetUserInfoInputDTO) -> GetUserInfoOutputDTO:
        if not await self.user_gateway.is_user_exists(input_dto.email):
            raise UserError(f'Пользователь не найден')

        user = await self.user_gateway.get_user_by_email(input_dto.email)
        return GetUserInfoOutputDTO(result=user)


class RegisterUserUseCase(Interactor[RegisterUserInputDTO, RegisterUserOutputDTO]):
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: RegisterUserInputDTO) -> RegisterUserOutputDTO:
        is_user_already_registered: bool = await self.user_gateway.is_user_exists(input_dto.email)

        if is_user_already_registered:
            raise UserError(f'Пользователь с электронной почтой \"{input_dto.email}\" уже существует.')

        new_user = UserEntity(
            id=None,
            name=input_dto.username,
            email=input_dto.email,
            refresh_token=None,
            refresh_token_expires_at=None,
            registered_at=datetime.now()
        )
        registered_user = await self.user_gateway.register_user(new_user)
        return RegisterUserOutputDTO(result=registered_user)


class LoginUserUseCase(Interactor[LoginUserInputDTO, LoginUserOutputDTO]):
    def __init__(self, settings: Settings, token_provider: TokenProvider, user_gateway: UserGateway):
        self.settings = settings
        self.token_provider = token_provider
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: LoginUserInputDTO) -> LoginUserOutputDTO:
        user_exists: bool = await self.user_gateway.is_user_exists(input_dto.email)

        if not user_exists:
            raise UserError('Пользователь не найден')

        otp = await self.user_gateway.get_last_otp(input_dto.email)

        if input_dto.one_time_password == otp.password or otp.expires_at > datetime.now():
            raise UserError('Одноразовый пароль неверен или просрочен')

        user = await self.user_gateway.get_user_by_email(input_dto.email)
        token_pair = await self.token_provider.create_token_pair(user)
        user.refresh_token = token_pair.refresh_token
        user.refresh_token_expires_at = token_pair.expires_at
        await self.user_gateway.update_user(user)
        return LoginUserOutputDTO(result=token_pair)
