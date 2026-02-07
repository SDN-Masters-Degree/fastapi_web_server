from datetime import datetime

from pydantic import BaseModel

from audio_spoof_detection_service.domain.types_and_consts import AudioResult


class AudioResponse(BaseModel):
    result: AudioResult


class AudioMetaInfo(BaseModel):
    id: int
    name: str
    analyze_result: AudioResult | None
    created_at: datetime


class AudioMetaInfoList(BaseModel):
    audio_meta_infos: list[AudioMetaInfo]


class DeleteAudioMetaInfoResponse(BaseModel):
    status: bool
