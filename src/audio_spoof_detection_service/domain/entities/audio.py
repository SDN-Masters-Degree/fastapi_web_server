from typing import BinaryIO
from dataclasses import dataclass
from datetime import datetime

from audio_spoof_detection_service.domain.common.entity import Entity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult


@dataclass
class AudioMetaInfoEntity(Entity):
    id: int | None
    user_id: int | None
    name: str
    analyze_result: AudioResult | None
    created_at: datetime


@dataclass
class AudioEntity(Entity):
    file: BinaryIO
    meta_info: AudioMetaInfoEntity
