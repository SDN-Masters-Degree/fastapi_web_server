from typing import BinaryIO
from dataclasses import dataclass

from audio_spoof_detection_service.domain.entities.audio import AudioMetaInfoEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult


@dataclass(frozen=True)
class CheckAudioSpoofInputDTO:
    audiofile: BinaryIO
    audiofile_name: str
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


@dataclass(frozen=True)
class GetAudioMetaInfoInputDTO:
    user_id: int
    audiofile_name: str


@dataclass(frozen=True)
class GetAudioMetaInfoOutputDTO:
    audio_info: AudioMetaInfoEntity


@dataclass(frozen=True)
class DeleteAudioMetaInfoInputDTO:
    user_id: int
    audiofile_name: str


@dataclass(frozen=True)
class DeleteAudioMetaInfoOutputDTO:
    status: bool
