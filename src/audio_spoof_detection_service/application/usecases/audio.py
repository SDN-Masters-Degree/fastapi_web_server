from audio_spoof_detection_service.domain.common.interactor import Interactor
from audio_spoof_detection_service.domain.entities.audio import AudioEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult
from audio_spoof_detection_service.application.contracts.audio import (
    CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO
)
from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.application.business_rules.audio import IsValidAudioFileRule


class CheckAudioSpoofUseCase(Interactor[CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO]):
    def __init__(self, cnn_model_gateway: CnnNeuralModelGateway,
                 is_valid_audio_business_rule: IsValidAudioFileRule):
        self.cnn_model_gateway = cnn_model_gateway
        self.is_valid_audio_business_rule = is_valid_audio_business_rule

    async def __call__(self, input_dto: CheckAudioSpoofInputDTO) -> CheckAudioSpoofOutputDTO:
        audio = AudioEntity(file=input_dto.audio_file, file_name=input_dto.audio_file_name)
        await self.is_valid_audio_business_rule(audio)
        sigmoid_val = await self.cnn_model_gateway.predict(audio)
        result = AudioResult.fake if sigmoid_val > 0.5 else AudioResult.real

        return CheckAudioSpoofOutputDTO(result=result)
