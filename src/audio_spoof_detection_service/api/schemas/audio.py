from pydantic import BaseModel

from audio_spoof_detection_service.domain.types_and_consts import AudioResult


class AudioResponse(BaseModel):
    result: AudioResult
