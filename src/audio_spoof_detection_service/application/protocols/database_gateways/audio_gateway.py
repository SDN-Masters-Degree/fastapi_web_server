from typing import Protocol

from audio_spoof_detection_service.domain.entities.audio import AudioMetaInfoEntity


class AudioMetaInfoGateway(Protocol):
    async def add_audio_meta_info(self, audio: AudioMetaInfoEntity) -> AudioMetaInfoEntity:
        raise NotImplementedError()

    async def get_audio_meta_info_by_id(self, audio_meta_info_id: int) -> AudioMetaInfoEntity:
        raise NotImplementedError()

    async def get_all_audio_meta_infos_by_user_id(self, user_id: int) -> list[AudioMetaInfoEntity]:
        raise NotImplementedError()

    async def update_audio_meta_info(self, audio: AudioMetaInfoEntity) -> None:
        raise NotImplementedError()

    async def delete_audio_meta_info(self, audio: AudioMetaInfoEntity) -> None:
        raise NotImplementedError()
