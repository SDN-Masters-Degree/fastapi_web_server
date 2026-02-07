from sqlalchemy import select, delete
from sqlalchemy.orm.session import Session

from audio_spoof_detection_service.application.protocols.database_gateways.audio_gateway import AudioMetaInfoGateway
from audio_spoof_detection_service.infrastructure.database_gateways.sqlalchemy.orm import AudioMetaInfoOrm
from audio_spoof_detection_service.domain.entities.audio import AudioMetaInfoEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult


class SqlAlchemyAudioMetaInfoGateway(AudioMetaInfoGateway):
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    async def __convert_entity_to_orm(audio_meta_info_entity: AudioMetaInfoEntity) -> AudioMetaInfoOrm:
        return AudioMetaInfoOrm(
            id=audio_meta_info_entity.id,
            user_id=audio_meta_info_entity.user_id,
            name=audio_meta_info_entity.name,
            analyze_result=audio_meta_info_entity.analyze_result,
            created_at=audio_meta_info_entity.created_at
        )

    @staticmethod
    async def __convert_orm_to_entity(audio_meta_info_orm: AudioMetaInfoOrm):
        return AudioMetaInfoEntity(
            id=audio_meta_info_orm.id,
            user_id=audio_meta_info_orm.user_id,
            name=audio_meta_info_orm.name,
            analyze_result=AudioResult(
                audio_meta_info_orm.analyze_result
            ) if audio_meta_info_orm.analyze_result is not None else None,
            created_at=audio_meta_info_orm.created_at
        )

    async def add_audio_meta_info(self, audio_meta_info: AudioMetaInfoEntity) -> AudioMetaInfoEntity:
        audio_meta_info_orm = await SqlAlchemyAudioMetaInfoGateway.__convert_entity_to_orm(audio_meta_info)
        self.session.add(audio_meta_info_orm)
        self.session.commit()
        audio_meta_info.id = audio_meta_info_orm.id
        return audio_meta_info

    async def get_audio_meta_info_by_user_id(self, user_id: int, audio_name: str) -> AudioMetaInfoEntity | None:
        get_audio_meta_info_by_id_query = (
            select(AudioMetaInfoOrm)
            .where((AudioMetaInfoOrm.id == user_id) & (AudioMetaInfoOrm.name == audio_name))
        )
        result = self.session.execute(get_audio_meta_info_by_id_query)
        audio_meta_info_orm: AudioMetaInfoOrm = result.scalar()

        if audio_meta_info_orm is None:
            return None

        audio_meta_info_entity = await SqlAlchemyAudioMetaInfoGateway.__convert_orm_to_entity(audio_meta_info_orm)
        return audio_meta_info_entity

    async def get_all_audio_meta_infos_by_user_id(self, user_id: int) -> list[AudioMetaInfoEntity]:
        get_all_audio_meta_infos_by_user_id_query = select(AudioMetaInfoOrm).where(AudioMetaInfoOrm.user_id == user_id)
        result = self.session.execute(get_all_audio_meta_infos_by_user_id_query)
        audio_meta_infos_orm = result.scalars()
        return [
            await SqlAlchemyAudioMetaInfoGateway.__convert_orm_to_entity(audio_meta_info_orm)
            for audio_meta_info_orm in audio_meta_infos_orm
        ]

    async def update_audio_meta_info(self, audio_meta_info: AudioMetaInfoEntity) -> None:
        audio_meta_info_orm = await SqlAlchemyAudioMetaInfoGateway.__convert_entity_to_orm(audio_meta_info)
        self.session.merge(audio_meta_info_orm)
        self.session.commit()

    async def delete_audio_meta_info(self, user_id: int, audio_name: str) -> None:
        delete_audio_info_stmt = (
            delete(AudioMetaInfoOrm)
            .where((AudioMetaInfoOrm.user_id == user_id) & (AudioMetaInfoOrm.name == audio_name))
        )
        self.session.execute(delete_audio_info_stmt)
        self.session.commit()
