from typing import BinaryIO
from dataclasses import dataclass

from audio_spoof_detection_service.domain.common.entity import Entity


@dataclass
class AudioEntity(Entity):
    file: BinaryIO
    file_name: str
