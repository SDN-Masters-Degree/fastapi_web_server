from typing import BinaryIO
from dataclasses import dataclass

from audio_spoof_detection_service.domain.types_and_consts import AudioResult


@dataclass(frozen=True)
class CheckAudioSpoofInputDTO:
    audio_file: BinaryIO
    audio_file_name: str


@dataclass(frozen=True)
class CheckAudioSpoofOutputDTO:
    result: AudioResult
