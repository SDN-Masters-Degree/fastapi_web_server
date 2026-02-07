import hashlib
from datetime import datetime, timezone

from audio_spoof_detection_service.application.common.interactor import Interactor
from audio_spoof_detection_service.application.protocols.database_gateways.user_gateway import UserGateway
from audio_spoof_detection_service.application.protocols.providers.token_provider import TokenProvider
from audio_spoof_detection_service.application.contracts.user import (
    RegisterUserInputDTO, RegisterUserOutputDTO, LoginUserInputDTO, LoginUserOutputDTO, LogoutUserInputDTO,
    LogoutUserOutputDTO, GetUserInfoInputDTO, GetUserInfoOutputDTO, RefreshUserTokensInputDTO,
    RefreshUserTokensOutputDTO
)
from audio_spoof_detection_service.domain.entities.user import UserEntity
from audio_spoof_detection_service.domain.error import UserError


class RegisterUserUseCase(Interactor[RegisterUserInputDTO, RegisterUserOutputDTO]):
    def __init__(self, user_gateway: UserGateway):
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: RegisterUserInputDTO) -> RegisterUserOutputDTO:
        is_user_already_registered: bool = await self.user_gateway.is_user_exists(input_dto.email)

        if is_user_already_registered:
            raise UserError(f'Пользователь с электронной почтой \"{input_dto.email}\" уже существует.')

        encoded_password: bytes = input_dto.password.encode()
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        new_user = UserEntity(
            id=None,
            name=input_dto.username,
            email=input_dto.email,
            hashed_password=hashed_password,
            refresh_token=None,
            registered_at=datetime.now(tz=timezone.utc)
        )
        registered_user = await self.user_gateway.register_user(new_user)
        return RegisterUserOutputDTO(user=registered_user)


class LoginUserUseCase(Interactor[LoginUserInputDTO, LoginUserOutputDTO]):
    def __init__(self, token_provider: TokenProvider, user_gateway: UserGateway):
        self.token_provider = token_provider
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: LoginUserInputDTO) -> LoginUserOutputDTO:
        user_exists: bool = await self.user_gateway.is_user_exists(input_dto.email)

        if not user_exists:
            raise UserError('Пользователь не найден.')

        user = await self.user_gateway.get_user_by_email(input_dto.email)
        hashed_password = hashlib.sha256(input_dto.password.encode()).hexdigest()

        if hashed_password != user.hashed_password:
            raise UserError('Неверный пароль')

        access_token = await self.token_provider.generate_access_token(user)
        refresh_token = await self.token_provider.generate_refresh_token(user)
        user.refresh_token = refresh_token
        await self.user_gateway.update_user(user)
        return LoginUserOutputDTO(access_token=access_token, refresh_token=refresh_token)


class LogoutUserUseCase(Interactor[LogoutUserInputDTO, LogoutUserOutputDTO]):
    def __init__(self, token_provider: TokenProvider, user_gateway: UserGateway):
        self.token_provider = token_provider
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: LogoutUserInputDTO) -> LogoutUserOutputDTO:
        refresh_token_payload = await self.token_provider.verify_token(input_dto.refresh_token)

        if not refresh_token_payload:
            raise UserError('Ошибка при верификации refresh токена.')

        if refresh_token_payload.type != 'refresh':
            raise UserError('Тип предоставленного токена не является типом "refresh".')

        email = refresh_token_payload.sub
        user = await self.user_gateway.get_user_by_email(email)
        user.refresh_token = None
        await self.user_gateway.update_user(user)
        return LogoutUserOutputDTO(success=True)


class GetUserInfoUseCase(Interactor[GetUserInfoInputDTO, GetUserInfoOutputDTO]):
    def __init__(self, token_provider: TokenProvider, user_gateway: UserGateway):
        self.token_provider = token_provider
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: GetUserInfoInputDTO) -> GetUserInfoOutputDTO:
        refresh_token_payload = await self.token_provider.verify_token(input_dto.access_token)

        if not refresh_token_payload:
            raise UserError('Ошибка при валидации refresh токена.')

        email = refresh_token_payload.sub

        if not await self.user_gateway.is_user_exists(email):
            raise UserError(f'Пользователь не найден')

        user = await self.user_gateway.get_user_by_email(email)
        return GetUserInfoOutputDTO(user=user)


class RefreshUserTokensUseCase(Interactor[RefreshUserTokensInputDTO, RefreshUserTokensOutputDTO]):
    def __init__(self, token_provider: TokenProvider, user_gateway: UserGateway):
        self.token_provider = token_provider
        self.user_gateway = user_gateway

    async def __call__(self, input_dto: RefreshUserTokensInputDTO) -> RefreshUserTokensOutputDTO:
        refresh_token_payload = await self.token_provider.verify_token(input_dto.refresh_token)

        if refresh_token_payload is None:
            raise UserError('Ошибка при валидации refresh токена.')

        user = await self.user_gateway.get_user_by_email(refresh_token_payload.sub)

        if user is None:
            raise UserError('Пользователь не найден.')

        access_token = await self.token_provider.generate_access_token(user)
        refresh_token = await self.token_provider.generate_refresh_token(user)
        user.refresh_token = refresh_token
        await self.user_gateway.update_user(user)
        return RefreshUserTokensOutputDTO(access_token=access_token, refresh_token=refresh_token)
