from typing import AsyncIterable
from dishka import Provider, Scope, provide, AsyncContainer, make_async_container
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm.session import Session, sessionmaker
from onnxruntime import InferenceSession

from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.application.protocols.database_gateways.audio_gateway import AudioMetaInfoGateway
from audio_spoof_detection_service.application.protocols.database_gateways.user_gateway import UserGateway
from audio_spoof_detection_service.application.protocols.providers.token_provider import TokenProvider
from audio_spoof_detection_service.application.usecases.audio import (
    CheckAudioSpoofUseCase, GetAudioMetaInfosUseCase, GetAudioMetaInfoUseCase, DeleteAudioMetaInfoUseCase
)
from audio_spoof_detection_service.application.usecases.user import (
    RegisterUserUseCase, LoginUserUseCase, LogoutUserUseCase, GetUserInfoUseCase, RefreshUserTokensUseCase
)
from audio_spoof_detection_service.application.business_rules.audio import IsValidAudioFileRule
from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.neural_model_gateway import TorchCnnNeuralModelGateway
from audio_spoof_detection_service.infrastructure.database_gateways.sqlalchemy.audio_gateway import SqlAlchemyAudioMetaInfoGateway
from audio_spoof_detection_service.infrastructure.database_gateways.sqlalchemy.user_gateway import SqlAlchemyUserGateway
from audio_spoof_detection_service.infrastructure.providers.token_provider import JwtTokenProvider
from audio_spoof_detection_service.infrastructure.settings import Settings, create_settings_instance


class SettingsProvider(Provider):
    @provide(scope=Scope.APP, provides=Settings)
    async def provide_settings(self) -> Settings:
        return create_settings_instance()


class SqlAlchemyEngineProvider(Provider):
    @provide(scope=Scope.APP, provides=Engine)
    async def provide_sqlalchemy_engine(self, settings: Settings) -> Engine:
        return create_engine(url=settings.db_url, echo=False)


class SqlAlchemySessionProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=Session)
    async def provide_sqlalchemy_session(self, engine: Engine) -> AsyncIterable[Session]:
        session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

        with session_maker() as session:
            yield session


class OnnxSessionProvider(Provider):
    scope = Scope.APP

    @provide()
    async def provide_onnx_session(self, settings: Settings) -> InferenceSession:
        return InferenceSession(settings.cnn_model_path)


class GatewayProvider(Provider):
    scope = Scope.REQUEST
    torch_cnn_neural_model_provider = provide(TorchCnnNeuralModelGateway, provides=CnnNeuralModelGateway)
    audio_meta_info_gateway_provider = provide(SqlAlchemyAudioMetaInfoGateway, provides=AudioMetaInfoGateway)
    user_gateway_provider = provide(SqlAlchemyUserGateway, provides=UserGateway)


class ProviderProvider(Provider):
    scope = Scope.APP
    token_provider_provider = provide(JwtTokenProvider, provides=TokenProvider)


class UseCaseProvider(Provider):
    scope = Scope.REQUEST
    register_user_use_case_provider = provide(RegisterUserUseCase)
    login_user_use_case_provider = provide(LoginUserUseCase)
    logout_user_use_case_provider = provide(LogoutUserUseCase)
    get_user_info_use_case_provider = provide(GetUserInfoUseCase)
    refresh_user_tokens_use_case_provider= provide(RefreshUserTokensUseCase)
    check_spoof_use_case_provider = provide(CheckAudioSpoofUseCase)
    get_audio_meta_infos_use_case_provider = provide(GetAudioMetaInfosUseCase)
    get_audio_meta_info_user_case_provider = provide(GetAudioMetaInfoUseCase)
    delete_audio_meta_info_user_case_provider = provide(DeleteAudioMetaInfoUseCase)


class BusinessRuleProvider(Provider):
    scope = Scope.REQUEST
    validate_audio_provider = provide(IsValidAudioFileRule)


def create_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SqlAlchemyEngineProvider(),
        SqlAlchemySessionProvider(),
        OnnxSessionProvider(),
        GatewayProvider(),
        ProviderProvider(),
        UseCaseProvider(),
        BusinessRuleProvider()
    )
