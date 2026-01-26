from typing import BinaryIO
from dataclasses import dataclass

from audio_spoof_detection_service.domain.entities.audio import AudioMetaInfoEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult


@dataclass(frozen=True)
class CheckAudioSpoofInputDTO:
    audio_file: BinaryIO
    audio_file_name: str
    user_id: int


@dataclass(frozen=True)
class CheckAudioSpoofOutputDTO:
    result: AudioResult


@dataclass(frozen=True)
class GetAudioMetaInfosInputDTO:
    user_id: int


@dataclass(frozen=True)
class GetAudioMetaInfosOutputDTO:
    result: list[AudioMetaInfoEntity]
