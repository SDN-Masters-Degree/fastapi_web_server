from typing import Protocol

from audio_spoof_detection_service.domain.entities.audio import AudioEntity


class CnnNeuralModelGateway(Protocol):
    async def predict(self, audio: AudioEntity) -> float:
        raise NotImplementedError()
