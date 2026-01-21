from typing import Protocol

from audio_spoof_detection_service.domain.entities.audio import AudioEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult


class CnnNeuralModelGateway(Protocol):
    async def predict(self, audio: AudioEntity) -> AudioResult:
        raise NotImplementedError()
