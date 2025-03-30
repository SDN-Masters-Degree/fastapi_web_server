from typing import BinaryIO
from dataclasses import dataclass

from audio_spoof_detection_service.domain.common.base_entity import BaseEntity


@dataclass
class AudioEntity(BaseEntity):
    file: BinaryIO
