from dishka import Provider, Scope, provide, AsyncContainer, make_async_container
from onnxruntime import InferenceSession

from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.application.usecases.audio import CheckAudioSpoofUseCase
from audio_spoof_detection_service.application.business_rules.audio import IsValidAudioFileRule
from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.neural_model_gateway import TorchCnnNeuralModelGateway
from audio_spoof_detection_service.infrastructure.settings import Settings, create_settings_instance


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide()
    async def get_settings(self) -> Settings:
        return create_settings_instance()


class SessionProvider(Provider):
    scope = Scope.APP

    @provide()
    async def get_session(self, settings: Settings) -> InferenceSession:
        return InferenceSession(settings.cnn_model_path)


class GatewayProvider(Provider):
    scope = Scope.REQUEST

    torch_cnn_neural_model_provider = provide(TorchCnnNeuralModelGateway, provides=CnnNeuralModelGateway)


class UseCaseProvider(Provider):
    scope = Scope.REQUEST

    check_spoof_use_case_provider = provide(CheckAudioSpoofUseCase)


class BusinessRuleProvider(Provider):
    scope = Scope.REQUEST

    validate_audio_provider = provide(IsValidAudioFileRule)


def create_container() -> AsyncContainer:
    return make_async_container(
        SettingsProvider(),
        SessionProvider(),
        GatewayProvider(),
        UseCaseProvider(),
        BusinessRuleProvider()
    )
