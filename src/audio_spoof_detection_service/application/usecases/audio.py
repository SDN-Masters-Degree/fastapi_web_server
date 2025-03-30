from audio_spoof_detection_service.domain.common.interactor import Interactor
from audio_spoof_detection_service.domain.entities.audio import AudioEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult
from audio_spoof_detection_service.application.contracts.audio import (
    CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO
)
from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway


class CheckAudioSpoofUseCase(Interactor[CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO]):
    def __init__(self, cnn_model_gateway: CnnNeuralModelGateway):
        self.cnn_model_gateway = cnn_model_gateway

    async def __call__(self, input_dto: CheckAudioSpoofInputDTO) -> CheckAudioSpoofOutputDTO:
        audio = AudioEntity(file=input_dto.audio_file)
        # TODO: check audio params
        sigmoid_val = await self.cnn_model_gateway.predict(audio)
        result = AudioResult.fake if sigmoid_val > 0.5 else AudioResult.real

        return CheckAudioSpoofOutputDTO(result=result)
